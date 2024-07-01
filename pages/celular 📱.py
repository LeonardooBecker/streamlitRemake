"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 08/09/2023
    Descrição: Painel de visualização dos dados do Estudo Naturalístico de Direção Brasileiro
    Link para o painel: https://painelndsbr.streamlit.app
    Link para o repositório: https://github.com/LeonardooBecker/streamlit

"""

import streamlit as st
import plotly.express as px
import altair as alt

# Processamento de dados
from local_libs.alteraNomes import *
from local_libs.preencheMapa import *
from local_libs.corrigeFiltros import *
from local_libs.completaQuery import *
from local_libs.inicializaValores import *

# custom components
from components.titulo import *
from components.rodape import *

# Operação db
from postgresql.query import *

with open("./css/style.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

def main():
    st.logo("https://www.inf.ufpr.br/lbo21/images/logoBranca.png")
    
    my_map = folium.Map(
        location=[-25.442027, -49.269582], zoom_start=12, tiles="CartoDB positron"
    )

    # Dicionario { chave : valor } contendo os parametros de interesse
    dicionario = {
        "faixaetaria": "",
        "sexo": "",
        "categoria": "",
        "hctb": "",
        "weekday": "",
        "action": "",
        "condutor": "",
        "idviagem": "",
    }
    
    # Dicionário que relaciona as chaves do dicionário com as tabelas e colunas do banco de dados ( simulando mapeamento )
    dictDescricaoParametros = {
        "faixaetaria": {"tabelas": ["viagem", "condutor"], "coluna": "faixaetaria"},
        "sexo": {"tabelas": ["viagem", "condutor"], "coluna": "sexo"},
        "categoria": {"tabelas": ["viagem", "condutor"], "coluna": "categoria"},
        "hctb": {"tabelas": ["hierarquiactb"], "coluna": "descricao"},
        "weekday": {"tabelas": ["diasemanal"], "coluna": "descricao"},
        "action": {"tabelas": ["acao"], "coluna": "descricao"},
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

    for chave in dicionario:
        if chave == "action":
            st.sidebar.selectbox(formataNome(chave),options=st.session_state[chave],format_func=lambda x: tradutorEnPt(x),key=f"{chave}SELECT",)
        elif chave == "weekday":
            st.sidebar.selectbox(formataNome(chave),options=transformaWeekday(st.session_state[chave]),key=f"{chave}SELECT",)
        elif chave == "categoria" or chave == "sexo":
            st.sidebar.radio(formataNome(chave),options=st.session_state[chave],key=f"{chave}SELECT",)
        else:
            st.sidebar.selectbox(formataNome(chave),options=st.session_state[chave],key=f"{chave}SELECT",)

    # Botão de atualização da página
    if st.sidebar.button("Atualizar página"):
        st.session_state.clear()
        st.experimental_rerun()

    # Título da página
    titulo(
        "Estudo Naturalístico de Direção Brasileiro - Indicadores sobre o uso do celular ao volante"
    )

    # ---------------------------------------------
    separaConteudo()
    # Calculo e apresentação dos indicadores na box superior                 

    tabelaBaseSQL = f"""
            WITH dadosFiltrados as(
                SELECT pickup, umpyn, wsb, velkmh, idacao, idbairro FROM SegundoRegistrado sreg
                {tabelaCompletaJoinFiltros(dicionario, dictDescricaoParametros)}     
                WHERE tempovalido=true
            )
            """

    dadosEspecificosSQL = """
                            SELECT COALESCE(CAST(SUM(CASE WHEN df.umpyn=TRUE THEN df.velkmh ELSE 0 END)AS FLOAT) /
                                            NULLIF(SUM(CASE WHEN df.umpyn=TRUE THEN 1 ELSE 0 END),0),0) as usoscelular,

                                    COALESCE(CAST(SUM(CASE WHEN df.umpyn=FALSE THEN df.velkmh ELSE 0 END)AS FLOAT) /
                                                NULLIF(SUM(CASE WHEN df.umpyn=FALSE THEN 1 ELSE 0 END),0),0) as semusocelular,

                                    COALESCE(CAST(SUM(CASE WHEN df.pickUp = TRUE THEN 1 ELSE 0 END) AS FLOAT) /
                                                NULLIF((CAST(COUNT(*) AS FLOAT)/3600),0),0) AS frequsocelular,

                                    COALESCE(CAST(SUM(CASE WHEN df.umpyn=TRUE THEN 1 ELSE 0 END) AS FLOAT) /
                                                NULLIF((COUNT(*)),0),0)*100 AS percentUso
                            FROM dadosFiltrados df
                            """

    tabelaResultados = retornaConsulta(tabelaBaseSQL + dadosEspecificosSQL)

    velDuranteUso = round(tabelaResultados.loc[0, "usoscelular"], 2)
    velSemUso = round(tabelaResultados.loc[0, "semusocelular"], 2)
    freqUsoCelular = round(tabelaResultados.loc[0, "frequsocelular"], 2)
    percentUso = round(tabelaResultados.loc[0, "percentuso"], 2)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Velocidade média durante o uso (km/h)", velDuranteUso)
    with col2:
        st.metric("Velocidade média sem o uso (km/h)", velSemUso)
    with col3:
        st.metric("Frequência do uso do celular  (usos/h)", freqUsoCelular)
    with col4:
        st.metric("Percentual do tempo de viagem usando o celular", str(percentUso) + "%")

    # ---------------------------------------------
    separaConteudo()
    # Gráfico de setores

    qry = f""" SELECT a.descricao as descricao, COUNT(*) as total FROM dadosfiltrados df
                INNER JOIN Acao a ON df.IdAcao = a.Id
                WHERE a.descricao != 'NAN'
                GROUP BY (a.descricao,df.idAcao)"""

    tabelaFiltrada = retornaConsulta(tabelaBaseSQL + qry)
    tabelaFiltrada.loc[:, "descricao"] = tabelaFiltrada["descricao"].apply(tradutorEnPt)
    data = {
        "Tipo de uso": tabelaFiltrada["descricao"],
        "Quantidade de uso": tabelaFiltrada["total"],
    }
    st.subheader("Distribuição dos tipos de uso do celular (% do tempo)")
    fig = px.pie(data, values="Quantidade de uso", names="Tipo de uso", height=300)
    st.write(fig)

    # ---------------------------------------------
    separaConteudo()
    # Gráfico de barras - Cidades

    qry = f""" SELECT c.nome as descricao, CAST(SUM(CASE WHEN pickup=TRUE THEN 1 ELSE 0 END) AS FLOAT)/(CAST(COUNT(*) AS FLOAT)/3600) as total FROM dadosfiltrados df
                INNER JOIN Bairro b on df.IdBairro = b.Id
                INNER JOIN Cidade c on b.IdCidade = c.Id
                GROUP BY (c.nome)
                ORDER BY total DESC
                """
    tabelaFiltrada = retornaConsulta(tabelaBaseSQL + qry)
    tabelaFiltrada = tabelaFiltrada[tabelaFiltrada["total"] != 0]
    tabelaFiltrada["total"] = tabelaFiltrada["total"].apply(lambda x: round(x, 2))
    tabelaFiltrada.columns = ["CIDADE", "FREQUENCIA"]
    st.subheader("Frequência de uso do celular por cidade (usos/h)")
    cidadebars = (
        alt.Chart(tabelaFiltrada)
        .mark_bar(width=20)
        .encode(x="FREQUENCIA", y=alt.Y("CIDADE", sort="-x"))
    )
    st.altair_chart(cidadebars)

    # ---------------------------------------------
    separaConteudo()
    # Gráfico de barras - Bairros
    qry = f""" SELECT b.nome as descricao, CAST(SUM(CASE WHEN pickup=TRUE THEN 1 ELSE 0 END) AS FLOAT)/(CAST(COUNT(*) AS FLOAT)/3600) as total FROM dadosfiltrados df
                INNER JOIN Bairro b on df.IdBairro = b.Id
                GROUP BY (b.nome)
                ORDER BY total DESC
                """
    tabelaFiltrada = retornaConsulta(tabelaBaseSQL + qry)
    tabelaFiltrada = tabelaFiltrada[tabelaFiltrada["total"] != 0]
    tabelaFiltrada["total"] = tabelaFiltrada["total"].apply(lambda x: round(x, 2))
    tabelaFiltrada.columns = ["BAIRRO", "FREQUENCIA"]
    st.subheader("Frequência de uso do celular por bairro (usos/h)")
    bairrobars = (
        alt.Chart(tabelaFiltrada)
        .mark_bar()
        .encode(x="FREQUENCIA", y=alt.Y("BAIRRO", sort="-x"))
    )
    st.altair_chart(bairrobars)

    # ---------------------------------------------
    separaConteudo()

    # Inserção do mapa
    selecionaMapa("Percentual do uso de celular", my_map, tabelaBaseSQL)

    # ---------------------------------------------
    separaConteudo()
    ## Rodapé da página

    rodape()


if __name__ == "__main__":
    main()
