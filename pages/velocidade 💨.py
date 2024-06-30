"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 08/09/2023
    Descrição: Painel de visualização dos dados do Estudo Naturalístico de Direção Brasileiro
    Link para o painel: https://painelndsbr.streamlit.app
    Link para o repositório: https://github.com/LeonardooBecker/streamlit

"""

import streamlit as st
import folium
import altair as alt


# Processamento de dados
from local_libs.alteraNomes import *
from local_libs.preencheMapa import * 
from local_libs.corrigeFiltros import *
from local_libs.radaresMapa import *
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
    my_map = folium.Map(location=[-25.442027, -49.269582],
                            zoom_start=12,tiles='CartoDB positron')

    map_radar = folium.Map(location=[-25.442027, -49.269582],
                        zoom_start=12)


    # Dicionario { chave : valor } contendo os parametros de interesse
    dicionario = {
        "hctb": "",
        "weekday": "",
        "sexo": "",
        "faixaetaria": "",
        "bairro":"",
        "cidade":"",
        "condutor": "",
        "idviagem": "",
    }
    
    # Dicionário que relaciona as chaves do dicionário com as tabelas e colunas do banco de dados ( simulando mapeamento )
    dictDescricaoParametros = {
        "hctb": {"tabelas": ["hierarquiactb"], "coluna": "descricao"},
        "weekday": {"tabelas": ["diasemanal"], "coluna": "descricao"},
        "sexo": {"tabelas": ["viagem", "condutor"], "coluna": "sexo"},
        "faixaetaria": {"tabelas": ["viagem", "condutor"], "coluna": "faixaetaria"},
        "bairro": {"tabelas": ["bairro"], "coluna": "nome"},
        "cidade": {"tabelas": ["bairro","cidade"], "coluna": "nome"},
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
    preencheVetorFiltro(dicionario,tabela)


    # Painel lateral - cada linha corresponde a um filtro possível
    for chave in dicionario:
        if chave == "action":
            st.sidebar.selectbox(label=formataNome(chave),options=st.session_state[chave],format_func=lambda x: tradutorEnPt(x),key=f"{chave}SELECT",)
        elif chave == "weekday":
            st.sidebar.selectbox(label=formataNome(chave),options=transformaWeekday(st.session_state[chave]),key=f"{chave}SELECT",)
        elif chave == "sexo":
            st.sidebar.radio(label=formataNome(chave),options=st.session_state[chave],key=f"{chave}SELECT",)
        else:
            st.sidebar.selectbox(label=formataNome(chave),options=st.session_state[chave],key=f"{chave}SELECT",)


    # Botão de atualização da página
    if st.sidebar.button('Atualizar página'):
        st.session_state.clear()
        st.experimental_rerun()


    ## Título da página
    titulo("Estudo Naturalístico de Direção Brasileiro - Indicadores sobre excesso de velocidade")

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
    dadosEspecificosSQL = """
                            SELECT val1, val2, CAST(val1 AS FLOAT)/CAST(val2 AS FLOAT) as val3 FROM
                            (
                                SELECT 
                                    (   
                                        SELECT
                                        CAST(SUM(CASE WHEN CAST(df.velkmh AS FLOAT) >= CAST(lv.velocidade AS FLOAT) THEN 1 ELSE 0 END) AS FLOAT)
                                        FROM DadosFiltrados df
                                        INNER JOIN LimiteVelocidade lv ON df.IdLimiteVelocidade = lv.Id
                                        WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI'
                                    ) / CAST(COUNT(*) AS FLOAT) as val1,

                                    (   
                                        SELECT
                                        CAST(SUM(CASE WHEN CAST(df.velkmh AS FLOAT) >= (CAST(lv.velocidade AS FLOAT)-10) THEN 1 ELSE 0 END) AS FLOAT)
                                        FROM DadosFiltrados df
                                        INNER JOIN LimiteVelocidade lv ON df.IdLimiteVelocidade = lv.Id
                                        WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI'
                                    ) / CAST(COUNT(*) AS FLOAT) as val2
                                FROM dadosFiltrados df
                            ) tab
                            """
    dadosEspecificosSQL = """
                            SELECT percentualexcesso, percentualoportunidade FROM
                            (
                                SELECT
                                    CAST(SUM(CASE WHEN CAST(df.velkmh AS FLOAT) >= CAST(lv.velocidade AS FLOAT) THEN 1 ELSE 0 END) AS FLOAT) as percentualexcesso,
                                    CAST(SUM(CASE WHEN CAST(df.velkmh AS FLOAT) >= (CAST(lv.velocidade AS FLOAT)-10) THEN 1 ELSE 0 END) AS FLOAT) as percentualoportunidade
                                FROM dadosFiltrados df
                                INNER JOIN LimiteVelocidade lv ON df.IdLimiteVelocidade = lv.Id
                                WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI'
                                UNION
                                SELECT
                                    CAST(COUNT(*) AS FLOAT),
                                    CAST(COUNT(*) AS FLOAT)
                                FROM dadosfiltrados
                            ) tab
                            """

    tabelaResultados = retornaConsulta(tabelaBaseSQL + dadosEspecificosSQL)
    percentualExcesso = round(tabelaResultados.loc[0, "percentualexcesso"]/tabelaResultados.loc[1, "percentualexcesso"]*100, 2)
    percentualOportunidade = round(tabelaResultados.loc[0, "percentualoportunidade"]/tabelaResultados.loc[1, "percentualoportunidade"]*100, 2)
    percentualExcessoCorrigido = round(tabelaResultados.loc[0, "percentualexcesso"]/tabelaResultados.loc[0, "percentualoportunidade"]*100, 2)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Percentual do tempo sob excesso de velocidade em relação ao tempo total de viagem", str(
            percentualExcesso)+"%")
    with col2:
        st.metric("Percentual do tempo de viagem com oportunidade de excesso de velocidade", str(
            percentualOportunidade)+"%")
    with col3:
        st.metric("Percentual do tempo sob excesso de velocidade em relação ao tempo de viagem*",
                str(percentualExcessoCorrigido)+"%")
        
    #---------------------------------------------
    separaConteudo()

    # Gráfico de barras - Cidades
    qry = f""" SELECT   c.nome as descricao, 
                        COALESCE(CAST(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= CAST(lv.velocidade AS FLOAT) THEN 1 ELSE 0 END) AS FLOAT) /
                                NULLIF(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= (CAST(lv.velocidade AS FLOAT)-10) THEN 1 ELSE 0 END),0)*100,0) AS total
                        FROM dadosfiltrados df
                INNER JOIN Bairro b on df.IdBairro = b.Id
                INNER JOIN Cidade c on b.IdCidade = c.Id
                INNER JOIN LimiteVelocidade lv on df.IdLimiteVelocidade = lv.Id
                WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI' AND c.nome != 'NPI'
                GROUP BY (c.nome)
                ORDER BY total DESC
                """
    tabelaFiltrada = retornaConsulta(tabelaBaseSQL + qry)
    tabelaFiltrada = tabelaFiltrada[tabelaFiltrada["total"] != 0]
    tabelaFiltrada["total"] = tabelaFiltrada["total"].apply(lambda x: round(x, 2))
    tabelaFiltrada.columns = ["Cidade", "Percentual"]
    st.subheader("Percentual do tempo sob excesso de velocidade por cidade*")
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
                        COALESCE(CAST(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= CAST(lv.velocidade AS FLOAT) THEN 1 ELSE 0 END) AS FLOAT) /
                            NULLIF(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= (CAST(lv.velocidade AS FLOAT)-10) THEN 1 ELSE 0 END),0)*100,0) AS total
                        FROM dadosfiltrados df
                INNER JOIN Bairro b on df.IdBairro = b.Id
                INNER JOIN LimiteVelocidade lv on df.IdLimiteVelocidade = lv.Id
                WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI' AND b.nome != 'NPI'
                GROUP BY (b.nome)
                ORDER BY total DESC
                """
    tabelaFiltrada = retornaConsulta(tabelaBaseSQL + qry)
    tabelaFiltrada = tabelaFiltrada[tabelaFiltrada["total"] != 0]
    tabelaFiltrada["total"] = tabelaFiltrada["total"].apply(lambda x: round(x, 2))
    tabelaFiltrada.columns = ["Bairro", "Percentual"]
    st.subheader("Percentual do tempo sob excesso de velocidade por bairro de Curitiba*")
    bairrobars = (
        alt.Chart(tabelaFiltrada)
        .mark_bar()
        .encode(x="Percentual", y=alt.Y("Bairro", sort="-x"))
    )
    st.altair_chart(bairrobars)

    #---------------------------------------------
    separaConteudo()

    # Gráfico de barras - Limite de velocidade
    qry = f""" SELECT   lv.velocidade as descricao,
                        COALESCE(CAST(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= CAST(lv.velocidade AS FLOAT) THEN 1 ELSE 0 END) AS FLOAT) /
                            NULLIF(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= (CAST(lv.velocidade AS FLOAT)-10) THEN 1 ELSE 0 END),0)*100,0) AS total
                        FROM dadosfiltrados df
                INNER JOIN LimiteVelocidade lv on df.IdLimiteVelocidade = lv.Id
                WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI'
                GROUP BY (lv.velocidade)
                ORDER BY total DESC
                """
    tabelaFiltrada = retornaConsulta(tabelaBaseSQL + qry)
    tabelaFiltrada = tabelaFiltrada[tabelaFiltrada["total"] != 0]
    tabelaFiltrada["total"] = tabelaFiltrada["total"].apply(lambda x: round(x, 2))
    tabelaFiltrada.columns = ["Limite da via", "Percentual"]
    st.subheader("Percentual do tempo sob excesso de velocidade segundo limite de velocidade regulamentar da via*")
    bairrobars = (
        alt.Chart(tabelaFiltrada)
        .mark_bar()
        .encode(x="Percentual", y=alt.Y("Limite da via", sort="-x"))
    )
    st.altair_chart(bairrobars)

    
    #---------------------------------------------
    separaConteudo()

    # Inserção do mapa e coloração do mapa sobre velocidade localizado na parte inferior da página
    selecionaMapa("Percentual do tempo sob excesso de velocidade*",my_map, tabelaBaseSQL)

    #---------------------------------------------
    separaConteudo()

    # Inserção do mapa e coloração do mapa sobre radares localizado na parte inferior da página
    insereMapaRadar(map_radar)

    #---------------------------------------------

    separaConteudo()
    ## Rodapé da página
    rodape()

if __name__ == "__main__":
    main()