"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 08/09/2023
    Descrição: Painel de visualização dos dados do Estudo Naturalístico de Direção Brasileiro
    Link para o painel: https://painelndsbr.streamlit.app
    Link para o repositório: https://github.com/LeonardooBecker/streamlit

"""

# Importação dos módulos
import streamlit as st
import sys 

# st.set_page_config(page_title="Estudo Naturalístico de Direção Brasileiro", layout="wide")
# navigation_tree = {
#     "Página Inicial": [
#         st.Page("pages/teste.py", title="inicio")
#     ],
#     "Reports": [
#         st.Page("pages/celular 📱.py", title="Celular"),
#         st.Page("pages/cinto 💺.py", title="Cinto"),
#     ]
# }
# nav = st.navigation(navigation_tree, position="sidebar")
# nav.run()


# Processamento de dados
sys.path.append('./local_libs')
from local_libs.alteraNomes import *
from local_libs.preencheMapa import *
from local_libs.corrigeFiltros import *
from local_libs.completaQuery import *
from local_libs.inicializaValores import *

# Componentes customizados
sys.path.append('./components')
from components.titulo import *
from components.rodape import *

# Operação db
sys.path.append('./postgres')
from postgres.query import *


# Importação do CSS
with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)


def main():

    my_map = folium.Map(location=[-25.442027, -49.269582],
                        zoom_start=12)

    # Dicionario { chave : valor } contendo os parametros de interesse
    dicionario={
        "faixaetaria":"",
        "hcwb":"",
        "hctb":"",
        "bairro":"",
        "cidade":"",
        "condutor":"",
        "idviagem":""
    }

    dictDescricaoParametros={
        "faixaetaria": {"tabelas": ["viagem", "condutor"], "coluna": "faixaetaria"},
        "hcwb": {"tabelas": ["hierarquiacwb"], "coluna": "descricao"},
        "hctb": {"tabelas": ["hierarquiactb"], "coluna": "descricao"},
        "bairro": {"tabelas": ["bairro"], "coluna": "nome"},
        "cidade": {"tabelas": ["bairro","cidade"], "coluna": "nome"},
        "condutor": {"tabelas": ["viagem", "condutor"], "coluna": "codigo"},
        "idviagem": {"tabelas": ["viagem"], "coluna": "identificadorviagem"},
    }
    
    # Inicialização dos valores
    for chave in dicionario:
        if chave+"SELECT" not in st.session_state:
            inicializaValores(dicionario)

    # Atualização do dicionário de acordo com os valores presentes em session_state
    atualizaDicionario(dicionario)

    tabelaFiltrosSQL = f"""
        SELECT * FROM (
            SELECT DISTINCT 
                {parteSelects(dictDescricaoParametros)}
            FROM SegundoRegistrado
                {parteJoins(dictDescricaoParametros)}
            WHERE tempoValido=true 
        ) subtab
        WHERE 1=1 {filtrosSelecionados(dicionario)}
    """

    tabela = retornaConsulta(tabelaFiltrosSQL)
    preencheVetorFiltro(dicionario,tabela)
    
    for chave in dicionario:
        st.sidebar.selectbox(formataNome(chave),options=st.session_state[chave], key=f"{chave}SELECT")

    # Botão de atualização da página
    if st.sidebar.button('Atualizar página'):
        st.session_state.clear()
        st.experimental_rerun()


    # Título da página

    titulo("Estudo Naturalístico de Direção Brasileiro")

    #---------------------------------------------

    separaConteudo()

    # Cálculo e apresentaçao dos parâmetros na box superior

    tabelaBaseSQL = f"""
        WITH dadosFiltrados as(
            SELECT * FROM SegundoRegistrado sreg
            {tabelaCompletaJoinFiltros(dicionario, dictDescricaoParametros)}      
            WHERE tempovalido=true
        )
        """

    valoresInteresseSQL = """
                    SELECT 
                            CAST(SUM(CASE WHEN df.pickUp = TRUE THEN 1 ELSE 0 END) AS FLOAT) /
                                                NULLIF((CAST(COUNT(*) AS FLOAT)/3600),0) AS frequsocelular,
                                                
                            (1 - CAST(SUM(CASE WHEN wsb=true OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT) /
                                                NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS percentWSB,
                            (SELECT COALESCE(CAST(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= CAST(lv.velocidade AS FLOAT) THEN 1 ELSE 0 END) AS FLOAT) /
                                NULLIF(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= (CAST(lv.velocidade AS FLOAT)-10) THEN 1 ELSE 0 END),0)*100,0) AS valor
                                FROM dadosfiltrados df
                                INNER JOIN LimiteVelocidade lv ON df.IdLimiteVelocidade = lv.Id
                                WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI') as pcExcesso,
                            
                            CAST(COUNT(*) AS FLOAT)/3600 AS tempoViagem
                    FROM dadosFiltrados df
                    """

    tableResultados= retornaConsulta(tabelaBaseSQL + valoresInteresseSQL)
    
    freqUsoCelular = round(tableResultados.loc[0,"frequsocelular"],2)
    percentWSB = round(tableResultados.loc[0,"percentwsb"],2)
    pcExcesso = round(tableResultados.loc[0,"pcexcesso"],2)
    tempoValido = round(tableResultados.loc[0,"tempoviagem"],2)
    

    col1, col2, col3, col4= st.columns(4)

    with col1:
        st.metric("Frequência de uso do celular (usos/hora)",freqUsoCelular)
    with col2:
        st.metric("Percentual do tempo de não uso do cinto de segurança",str(percentWSB)+"%")
    with col3:
        st.metric("Percentual do tempo sob excesso de velocidade*",str(pcExcesso)+"%")
    with col4:
        st.metric("Tempo de viagem (h)",tempoValido)


    #---------------------------------------------
    separaConteudo()
    
    # Coloração e inserção do mapa inferior assim como as opções de visualização disponível
    options=["Frequência de uso do celular (usos/hora)",
             "Percentual do tempo de não uso do cinto de segurança",
             "Percentual do tempo sob excesso de velocidade*"]

    st.selectbox("Selecione o parâmetro para ser preenchido o mapa:",
                    options, 
                    key="ESCOLHA")


    selecionaMapa(st.session_state["ESCOLHA"],my_map, tabelaBaseSQL)

    #---------------------------------------------
    separaConteudo()
    ## Rodapé da página
    rodape()

    #---------------------------------------------

if __name__ == "__main__":
    main()
