"""
    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Link para o repositório: https://github.com/LeonardooBecker/streamlit
"""

import streamlit as st
import streamlit.components.v1 as components

def tt(titulo):
    components.html(
        f"""
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            <div id="carouselExampleControls" class="carousel slide" data-ride="carousel" style="height:500px">
            <div class="carousel-inner">
                <div class="carousel-item active" style="background-color:transparent">
                    <h1 style="background-color:transparent">{titulo}</h1>
                </div>
                <div class="carousel-item">
                    <img class="d-block w-100" src="https://www.inf.ufpr.br/lbo21/images/logoBranca.png" alt="Segundo Slide">
                </div>
            </div>
            <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="sr-only">Anterior</span>
            </a>
            <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="sr-only">Próximo</span>
            </a>
            </div>
        """
    )
    
def titulo(titulo):
    # Use o f-string para inserir a variável no código HTML
    html_code = f"""
                <style>
                .titulo {{
                    display: flex;
                    flex-direction: row;
                    flex-wrap: wrap;
                }}
                #texto{{
                    padding: 10px;
                }}
                #logoNDS {{
                    display: block;
                    width: 350px;
                    height: fit-content;
                    margin: auto;
                    padding: 15px;
                }}
                </style>
                <div class="titulo">
                    <h1 style="font-size:42px; text-align:center">{titulo}</h1>
                </div>
                """

    st.markdown(html_code, unsafe_allow_html=True)

def separaConteudo():
    html_code = f"""
                <style>
                .separa-conteudo {{
                    border: none;
                    height: 2px;
                    background-color: cyan;
                    margin: 50px 150px 50px 150px;
                }}
                </style>
                <hr class="separa-conteudo">
                """
    st.markdown(html_code, unsafe_allow_html=True)