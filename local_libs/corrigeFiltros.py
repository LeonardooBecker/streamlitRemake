"""
    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Link para o repositório: https://github.com/LeonardooBecker/streamlit
"""

import pandas as pd
import streamlit as st
from alteraNomes import *
from unidecode import unidecode

# Para cada chave presente no dicionário verifica se o valor não é vazio para poder filtrar a tabela ( csv principal ) de acordo com o valor correspondente a chave
def atualizaTabela(dicionario,tabela):
    novaTabela=tabela
    for chave in dicionario:
        if(dicionario[chave]!=""):
            novaTabela = novaTabela[novaTabela[chave]==dicionario[chave]]
    return novaTabela

# Atualiza o dicionário para deixar de acordo com o valor encontrado em session_state
def atualizaDicionario(dicionario):
    for chave in dicionario:
        dicionario[chave]=st.session_state[chave+"SELECT"]

# Preenche os vetores de filtro de acordo com os dados presentes na tabela e os presentes no dicionário.
def preencheVetorFiltro(dicionario,tabela):
    tabela = atualizaTabela(dicionario,tabela)
    for chave in dicionario:
        dfParam = pd.DataFrame()
        dfParam[chave] = tabela[chave].drop_duplicates()
        dfParam["sorted"] = tabela[chave].apply(unidecode)
        if dicionario[chave]=="":
            dfParam.loc[-1] = "" * dfParam.shape[1]
        dfParam = dfParam.sort_values(by="sorted")
        vetorAuxiliar = dfParam[chave].tolist()
        st.session_state[chave] = vetorAuxiliar