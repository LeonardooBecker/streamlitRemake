"""
    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Link para o repositório: https://github.com/LeonardooBecker/streamlit
"""

import streamlit as st
import streamlit.components.v1 as components

def rodape():
    st.markdown("""
            <style>
            .back
            {
                padding: 30px;
                border-radius: 20px;
                background-color: #c8c8c8;
            }
            #infos {
                color: #353535;
            }
            #refs
            {
                color: #666666;
                margin: 30px;
            }
            .images {
                display: flex;
                flex-wrap: wrap;
            }
            .images img {
                width:30%;
                padding: 20px;
                flex: 1;
                object-fit: contain; 
            }
            </style>
            <div class="back">
                <div id="infos">
                    <p style="margin:2px; font-size: 14px;">Desenvolvedor: Leonardo Becker de Oliveira <a href="mailto:lbo21@inf.ufpr.br"> lbo21@inf.ufpr.br </a></p>
                    <p style="margin:2px; font-size: 14px;">Coordenador: Prof. Dr. Jorge Tiago Bastos <a href="mailto:jtbastos@ufpr.br"> jtbastos@ufpr.br </a></p>
                    <p style="margin:2px; font-size: 14px;">Financiamento: Universidade Federal do Paraná, Conselho Nacional de Desenvolvimento Científico e Tecnológico, Observatório Nacional de Segurança Viária e Mobi 7 - Soluções para Mobilidade.</p>
                    <p style="margin:2px; font-size: 14px;">Mais informações em <a href="http://www.tecnologia.ufpr.br/portal/ceppur/estudo-naturalistico-de-direcao-brasileiro/">Estudo Naturalístico de Direção Brasileiro - CEPPUR-UFPR</a> (Link para este endereço: <a href="http://www.tecnologia.ufpr.br/portal/ceppur/estudo-naturalistico-de-direcao-brasileiro/">http://www.tecnologia.ufpr.br/portal/ceppur/estudo-naturalistico-de-direcao-brasileiro/</a> )</p>
                </div>
                <div id="refs">     
                    <p style="font-size: 12px; margin:2px">* % do tempo sob excesso de velocidade em relação ao tempo de viagem com oportunidade de excesso de velocidade</p>
                    <p style="font-size: 12px; margin:2px"> Para referenciar este conteúdo: OLIVEIRA, Leonardo Becker; BASTOS, Jorge Tiago. Estudo Naturalístico de Direção Brasileiro: Painel de visualização. Curitiba 2023. Disponível em: <a href="https://painelndsbr.streamlit.app">Streamlit</a>. Acesso em: dia mês. ano. </p>
                </div>
                <div class="images">
                    <img src="https://www.inf.ufpr.br/lbo21/images/logoUFPR.jpg">
                    <img src="https://www.inf.ufpr.br/lbo21/images/logoCNPQ.jpg">
                    <img src="https://www.inf.ufpr.br/lbo21/images/logoONSV.png">
                </div>
            </div>
             """ , unsafe_allow_html=True
            )

def rodapea():
    # bootstrap 4 collapse example
    components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

        <style>
            .back
            {
                padding: 30px;
                border-radius: 20px;
                background-color: #c8c8c8;
            }
            #infos {
                color: #353535;
            }
            #refs
            {
                color: #666666;
                margin: 30px;
            }
            .images {
                display: flex;
                flex-wrap: wrap;
            }
            .images img {
                width:30%;
                padding: 20px;
                flex: 1;
                object-fit: contain; 
            }
        </style>
            <div class="back">
                <div id="infos">
                    <p style="margin:2px; font-size: 14px;">Desenvolvedor: Leonardo Becker de Oliveira <a href="mailto:lbo21@inf.ufpr.br"> lbo21@inf.ufpr.br </a></p>
                    <p style="margin:2px; font-size: 14px;">Coordenador: Prof. Dr. Jorge Tiago Bastos <a href="mailto:jtbastos@ufpr.br"> jtbastos@ufpr.br </a></p>
                    <p style="margin:2px; font-size: 14px;">Financiamento: Universidade Federal do Paraná, Conselho Nacional de Desenvolvimento Científico e Tecnológico, Observatório Nacional de Segurança Viária e Mobi 7 - Soluções para Mobilidade.</p>
                    <p style="margin:2px; font-size: 14px;">Mais informações em <a href="http://www.tecnologia.ufpr.br/portal/ceppur/estudo-naturalistico-de-direcao-brasileiro/">Estudo Naturalístico de Direção Brasileiro - CEPPUR-UFPR</a> (Link para este endereço: <a href="http://www.tecnologia.ufpr.br/portal/ceppur/estudo-naturalistico-de-direcao-brasileiro/">http://www.tecnologia.ufpr.br/portal/ceppur/estudo-naturalistico-de-direcao-brasileiro/</a> )</p>
                </div>
                <div id="refs">     
                    <p style="font-size: 12px; margin:2px">* % do tempo sob excesso de velocidade em relação ao tempo de viagem com oportunidade de excesso de velocidade</p>
                    <p style="font-size: 12px; margin:2px"> Para referenciar este conteúdo: OLIVEIRA, Leonardo Becker; BASTOS, Jorge Tiago. Estudo Naturalístico de Direção Brasileiro: Painel de visualização. Curitiba 2023. Disponível em: <a href="https://painelndsbr.streamlit.app">Streamlit</a>. Acesso em: dia mês. ano. </p>
                </div>
    <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
            <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>
            <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
            <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
        </ol>
        <div class="carousel-inner">
            <div class="carousel-item active">
            <img class="d-block w-100" src="https://www.inf.ufpr.br/lbo21/images/logoUFPR.jpg" alt="Primeiro Slide">
            </div>
            <div class="carousel-item">
            <img class="d-block w-100" src="https://www.inf.ufpr.br/lbo21/images/logoCNPQ.jpg" alt="Segundo Slide">
            </div>
            <div class="carousel-item">
            <img class="d-block w-100" src="https://www.inf.ufpr.br/lbo21/images/logoONSV.png" alt="Terceiro Slide">
            </div>
        </div>
        <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Anterior</span>
        </a>
        <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Próximo</span>
        </a>
    </div>
    </div>
    
    """,
    height=600,
)