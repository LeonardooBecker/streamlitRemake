import streamlit as st
from postgres.connect import *

connection = initConnection()

@st.cache_data
def retornaConsulta(query):
    return connection.query(query)