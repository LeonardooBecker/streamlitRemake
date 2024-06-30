import streamlit as st

# Inicialização dos valores de session_state, utilizado durante todo o código
def inicializaValores(dicionario):
    for chave in dicionario:
        st.session_state[chave+"SELECT"] = ""