import streamlit as st
from postgresql.connect import *

connection = initConnection()

@st.cache_data
def retornaConsulta(query):
    return connection.query(query)