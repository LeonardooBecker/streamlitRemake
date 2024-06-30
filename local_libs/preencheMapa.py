"""
    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Link para o repositório: https://github.com/LeonardooBecker/streamlit
"""

import pandas as pd
from branca.colormap import linear
from streamlit_folium import folium_static
import folium
import streamlit as st

# Operação db
from postgres.query import *

def filtraBairrosValido(x, dfCodigo):
    if x in dfCodigo["BAIRRO"].values:
        return x
    else:
        return None

def retornaCodigoBairro(x, dfCodigo):
    if x in dfCodigo["BAIRRO"].values:
        return dfCodigo[dfCodigo["BAIRRO"]==x]["CODIGO"].iloc[0]

# Preenche o mapa com os dados e cores de acordo com a escolha do usuário
def coloreMapa(escolha, my_map, tabelaBaseSQL):
    
    dfCodigo = pd.read_csv('./data/codigoBairros.csv', sep=',')

    condicaoExtra=""
    if (escolha == "Frequência de uso do celular (usos/hora)"):
        escolhaDefinidaSQL = """CAST(SUM(CASE WHEN df.pickUp = TRUE THEN 1 ELSE 0 END) AS FLOAT) / NULLIF((CAST(COUNT(*) AS FLOAT)/3600),0) AS valor"""
        legenda = "Frequência de uso do celular por hora"
        
    elif (escolha == "Percentual do tempo de não uso do cinto de segurança"):
        escolhaDefinidaSQL = """(1 - CAST(SUM(CASE WHEN wsb=true OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS valor"""
        legenda = "Percentual do tempo de não uso do cinto de segurança"    

    elif (escolha == "Percentual do tempo sob excesso de velocidade*"):
        condicaoExtra = """ INNER JOIN LimiteVelocidade lv ON df.idLimiteVelocidade = lv.id
                            WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI'"""
        escolhaDefinidaSQL = """COALESCE(CAST(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= CAST(lv.velocidade AS FLOAT) THEN 1 ELSE 0 END) AS FLOAT) /
                                NULLIF(SUM(CASE WHEN CAST(velkmh AS FLOAT) >= (CAST(lv.velocidade AS FLOAT)-10) THEN 1 ELSE 0 END),0)*100,0) AS valor"""
        legenda = "Percentual do tempo sob excesso de velocidade*"
        
    elif (escolha == "Percentual do uso de celular"):
        escolhaDefinidaSQL = """(CAST(SUM(CASE WHEN umpyn = TRUE THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS valor"""
        legenda = "Percentual do tempo de viagem usando o celular"
        
    elif (escolha == "Independente do limite"):
        escolhaDefinidaSQL = """(1 - CAST(SUM(CASE WHEN wsb=true OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS valor"""
        legenda = "Percentual do tempo de não uso do cinto de segurança"
        
    elif (escolha == "Acima do limite"):
        condicaoExtra = """ INNER JOIN LimiteVelocidade lv ON df.idLimiteVelocidade = lv.id
                            WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI' AND CAST(df.velKmh AS FLOAT) > CAST(lv.velocidade AS FLOAT)"""
        escolhaDefinidaSQL = """(1 - CAST(SUM(CASE WHEN wsb=true OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS valor"""
        legenda = "Percentual do tempo de não uso do cinto de segurança"
        
    elif (escolha == "Abaixo do limite"):
        condicaoExtra = """ INNER JOIN LimiteVelocidade lv ON df.idLimiteVelocidade = lv.id
                            WHERE lv.velocidade != '0' AND lv.velocidade != 'NPI' AND CAST(df.velKmh AS FLOAT) < CAST(lv.velocidade AS FLOAT)"""
        escolhaDefinidaSQL = """(1 - CAST(SUM(CASE WHEN wsb=true OR wsb IS NULL THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(CAST(COUNT(*) AS FLOAT),0))*100 AS valor"""
        legenda = "Percentual do tempo de não uso do cinto de segurança"

    contSQL = f"""
                SELECT 
                    b.nome as bairro,
                    {escolhaDefinidaSQL}
                FROM dadosFiltrados df
                INNER JOIN Bairro b ON df.idBairro = b.Id
                {condicaoExtra}
                GROUP BY b.nome
                """
    dfValores = retornaConsulta(tabelaBaseSQL+contSQL)

    bairros = pd.DataFrame()
    bairros["bairro"] = dfValores["bairro"].drop_duplicates().apply(lambda x: filtraBairrosValido(x, dfCodigo)).dropna()
    bairros["codigo"] = dfValores["bairro"].drop_duplicates().apply(lambda x: retornaCodigoBairro(x, dfCodigo)).dropna()
    bairros["pinta"] = dfValores["valor"].apply(lambda x: round(x,2))

    bairros.columns = ["Bairros", "Codigo", "Pinta"]
    
    maxValue = bairros["Pinta"].max() if bairros["Pinta"].max() > 0 else 1
    colormap = linear.YlOrRd_09.scale(0, maxValue)
    colormap.caption = legenda
    colormap.add_to(my_map)
    
    state_data = bairros

    choropleth = folium.Choropleth(
        geo_data='./data/bairros.geo.json',
        data=bairros,
        columns=['Codigo', 'Pinta'],
        key_on='feature.properties.codigo',
        fill_color="YlOrRd",
        fill_opacity=0.5,
        nan_fill_opacity=0,
        line_color="Gray",
        line_opacity=0.4
    )
    choropleth.geojson.add_to(my_map)

    state_data_indexed = state_data.set_index('Codigo')

    for s in choropleth.geojson.data['features']:
        if ((s['properties']['codigo']) in state_data['Codigo'].values):
            valor = s['properties']['codigo']
            s['properties']['valor'] = float(
                state_data_indexed.loc[valor, "Pinta"])
        else:
            s['properties']['valor'] = 0

    folium.GeoJsonTooltip(['nome', 'valor']).add_to(choropleth.geojson)


# Insere o mapa e sua respectiva legenda na página
def insereMapa(escolha, my_map):
    if (escolha == "Frequência de uso do celular (usos/hora)"):
        st.subheader("Mapa de calor representando a frequência de uso do celular por hora")

    if (escolha == "Percentual do tempo de não uso do cinto de segurança"):
        st.subheader("Mapa de calor representando o percentual do tempo sem o uso do cinto de segurança")

    if (escolha == "Percentual do tempo sob excesso de velocidade*"):
        st.subheader("Mapa de calor representando o percentual do tempo sob o excesso de velocidade*")
        
    if (escolha == "Percentual do uso de celular"):
        st.subheader("Percentual do tempo de viagem usando o celular segundo bairro de Curitiba")

    folium_static(my_map)

# Função mediadora para preencher e apresentar o mapa
@st.experimental_fragment
def selecionaMapa(opcaoEscolhidam, my_map, tabelaBaseSQL):
    coloreMapa(opcaoEscolhidam, my_map, tabelaBaseSQL)
    insereMapa(opcaoEscolhidam,my_map)
