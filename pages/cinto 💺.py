"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 08/09/2023
    Descrição: Painel de visualização dos dados do Estudo Naturalístico de Direção Brasileiro
    Link para o painel: https://painelndsbr.streamlit.app
    Link para o repositório: https://github.com/LeonardooBecker/streamlit

"""

import streamlit as st
import sys
import folium
import altair as alt

# Processamento de dados
sys.path.append('./local_libs')
from local_libs.alteraNomes import *
from local_libs.preencheMapa import * 
from local_libs.corrigeFiltros import *
from local_libs.completaQuery import *
from local_libs.inicializaValores import *


# Componentes customizados
from components.titulo import *
from components.rodape import *

# Operação db
from postgres.query import *

with open("./css/style.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

def main():
    st.logo("https://www.inf.ufpr.br/lbo21/images/logoBranca.png")
    
    my_map = folium.Map(location=[-25.442027, -49.269582],
                            zoom_start=12,tiles='CartoDB positron')


    # Dicionario { chave : valor } contendo os parametros de interesse
    dicionario = {
        "faixaetaria": "",
        "sexo": "",
        "condutor": "",
        "idviagem": "",
    }
    
    # Dicionário que relaciona as chaves do dicionário com as tabelas e colunas do banco de dados ( simulando mapeamento )
    dictDescricaoParametros = {
        "faixaetaria": {"tabelas": ["viagem", "condutor"], "coluna": "faixaetaria"},
        "sexo": {"tabelas": ["viagem", "condutor"], "coluna": "sexo"},
        "condutor": {"tabelas": ["viagem", "condutor"], "coluna": "codigo"},
        "idviagem": {"tabelas": ["viagem"], "coluna": "identificadorviagem"},
    }

    # Inicialização dos valores
    for chave in dicionario:
        if chave + "SELECT" not in st.session_state:
            inicializaValores(dicionario)

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

    preencheVetorFiltro(dicionario, tabela)

    # Painel lateral - cada linha corresponde a um filtro possível
    for chave in dicionario:
        if chave == "sexo":
            st.sidebar.radio(formataNome(chave), options=st.session_state[chave], key=f"{chave}SELECT")
        else:
            st.sidebar.selectbox(formataNome(chave),options=st.session_state[chave],key=f"{chave}SELECT")


    # Botão de atualização da página
    if st.sidebar.button('Atualizar página'):
        st.session_state.clear()
        st.experimental_rerun()
        
    # Título da página
    titulo("Estudo Naturalístico de Direção Brasileiro - Indicadores sobre o uso do cinto de segurança")

    ##---------------------------------------------
    separaConteudo()

    # Calculo e apresentação dos indicadores na box superior
    tabelaBaseSQL = f"""
        WITH dadosFiltrados as(
            SELECT * FROM SegundoRegistrado sreg
            {tabelaCompletaJoinFiltros(dicionario, dictDescricaoParametros)}     
            WHERE tempovalido=true
        )
    """
    dadosEspecificosSQL = f"""
            SELECT 
                (1 - CAST(SUM(CASE WHEN wsb=true OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT) /
                NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS percentwsb,
                
                CAST(SUM(CASE WHEN (wsb=TRUE OR wsb IS NULL) THEN df.velkmh ELSE 0 END) AS FLOAT) /
                NULLIF(CAST(SUM(CASE WHEN wsb=TRUE OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT),0) as vmusocinto,
                
                CAST(SUM(CASE WHEN wsb=FALSE THEN df.velkmh ELSE 0 END) AS FLOAT) /
                NULLIF(CAST(SUM(CASE WHEN wsb=FALSE THEN 1 ELSE 0 END) AS FLOAT),0) as vmsemcinto
            FROM dadosfiltrados df
    """
    tabelaResultados = retornaConsulta(tabelaBaseSQL + dadosEspecificosSQL)
    percentWsb = round(tabelaResultados.loc[0, "percentwsb"], 2)
    vmUsoCinto = round(tabelaResultados.loc[0, "vmusocinto"], 2)
    vmSemCinto = round(tabelaResultados.loc[0, "vmsemcinto"], 2)
    
    col1, col2, col3= st.columns(3)
    with col1:
        st.metric("Percentual do tempo de não uso do cinto de segurança", str(percentWsb)+"%")
    with col2:
        st.metric("Velocidade média com o uso do cinto (km/h)", vmUsoCinto)
    with col3:
        st.metric("Velocidade média sem o uso do cinto (km/h)", vmSemCinto)

    #---------------------------------------------
    separaConteudo()

    # Gráfico de barras - Hierarquia viária
    qry = f""" SELECT   h.descricao as descricao,
                        (1 - CAST(SUM(CASE WHEN wsb=true OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT) /
                NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS total
                FROM dadosfiltrados df
                INNER JOIN hierarquiactb h ON df.idhierarquiactb = h.id
                GROUP BY (h.descricao)"""

    tabelaFiltrada = retornaConsulta(tabelaBaseSQL + qry)
    tabelaFiltrada["total"] = tabelaFiltrada["total"].apply(lambda x: round(x, 2))
    tabelaFiltrada.columns = ["Hierarquia", "Percentual sem cinto"]
    tabelaFiltrada.set_index("Hierarquia", inplace=True)
    st.subheader("Percentual do tempo de viagem sem uso do cinto segundo hierarquia da via")
    st.bar_chart(tabelaFiltrada, x_label="Hierarquia CTB", y_label="Percentual (%)")


    #---------------------------------------------
    separaConteudo()


    # Gráfico de barras - Cidades

    qry = f""" SELECT   c.nome as descricao, 
                        (1 - CAST(SUM(CASE WHEN wsb=true OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT) /NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS total
                        FROM dadosfiltrados df
                INNER JOIN Bairro b on df.IdBairro = b.Id
                INNER JOIN Cidade c on b.IdCidade = c.Id
                GROUP BY (c.nome)
                ORDER BY total DESC
                """
    tabelaFiltrada = retornaConsulta(tabelaBaseSQL + qry)
    tabelaFiltrada = tabelaFiltrada[tabelaFiltrada["total"] != 0]
    tabelaFiltrada["total"] = tabelaFiltrada["total"].apply(lambda x: round(x, 2))
    tabelaFiltrada.columns = ["Cidade", "Percentual"]
    st.subheader("Percentual do tempo de viagem sem o uso do cinto de segurança segundo cidade")
    cidadebars = (
        alt.Chart(tabelaFiltrada)
        .mark_bar(width=20)
        .encode(x="Percentual", y=alt.Y("Cidade", sort="-x"))
    )
    st.altair_chart(cidadebars)

    #---------------------------------------------
    separaConteudo()

    # Gráfico de barras - Bairros
    qry = f""" SELECT   b.nome as descricao,
                        (1 - CAST(SUM(CASE WHEN wsb=true OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT) /NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS total
                        FROM dadosfiltrados df
                INNER JOIN Bairro b on df.IdBairro = b.Id
                GROUP BY (b.nome)
                ORDER BY total DESC
                """
    tabelaFiltrada = retornaConsulta(tabelaBaseSQL + qry)
    tabelaFiltrada = tabelaFiltrada[tabelaFiltrada["total"] != 0]
    tabelaFiltrada["total"] = tabelaFiltrada["total"].apply(lambda x: round(x, 2))
    tabelaFiltrada.columns = ["Bairro", "Percentual"]
    st.subheader("Percentual do tempo de viagem sem o uso do cinto de segurança segundo bairro")
    bairrobars = (
        alt.Chart(tabelaFiltrada)
        .mark_bar()
        .encode(x="Percentual", y=alt.Y("Bairro", sort="-x"))
    )
    st.altair_chart(bairrobars)

    #---------------------------------------------
    separaConteudo()

    # Inserção do mapa e coloração do mapa localizado na parte inferior da página
    st.subheader("Percentual do tempo de viagem sem o uso do cinto de segurança para bairros de Curitiba")
    options=["Independente do limite","Abaixo do limite","Acima do limite"]

    st.radio("Segundo limite de velocidade:",options, key="ESCOLHA")

    selecionaMapa(st.session_state["ESCOLHA"],my_map,tabelaBaseSQL)

    #---------------------------------------------
    separaConteudo()

    # Rodapé da página
    rodape()

if __name__ == "__main__":
    main()