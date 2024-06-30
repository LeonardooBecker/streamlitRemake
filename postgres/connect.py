import streamlit as st

@st.cache_resource
def initConnection():
    return st.connection("postgresql", type="sql")