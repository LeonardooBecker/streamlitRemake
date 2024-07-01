import streamlit as st
import psycopg2

@st.cache_resource
def initConnection():
    return st.connection("postgresql", type="sql")