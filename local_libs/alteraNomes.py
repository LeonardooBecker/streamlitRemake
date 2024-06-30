"""
    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Link para o repositório: https://github.com/LeonardooBecker/streamlit
"""

def formataNome(keyName):
    if(keyName=="condutor"):
        return "Condutor"
    elif(keyName=="bairro"):
        return "Bairro"
    elif(keyName=="cidade"):
        return "Cidade"
    elif(keyName=="faixaetaria"):
        return "Faixa etária do condutor"
    elif(keyName=="hctb"):
        return "Hierarquia viária (CTB)"
    elif(keyName=="hcwb"):
        return "Hierarquia viária (Curitiba)"
    elif(keyName=="idviagem"):
        return "Viagem"
    elif(keyName=="sexo"):
        return "Sexo"
    elif(keyName=="categoria"):
        return "Categoria"
    elif(keyName=="weekday"):
        return "Dia da semana"
    elif(keyName=="action"):
        return "Tipo de uso"
    else:
        return ""

def tradutorEnPt(word):
    if(word=="CHECKING/BROWSING"):
        return "CONFERINDO/NAVEGANDO"
    if(word=="ON-HOLDER"):
        return "USO NO SUPORTE"
    if(word=="HOLDING"):
        return "SEGURANDO"
    if(word=="TEXTING"):
        return "ENVIANDO MENSAGEM"
    if(word=="CALLING/VOICE MESSAGE"):
        return "LIGAÇÃO/MENSAGEM DE VOZ"
    if(word=="OTHER"):
        return "OUTROS"     
    if(word=="NPI"):
        return "NPI"
    return word


import streamlit as st
def transformaWeekday(weekdays):
    vetor=[]
    dias_ordenados = ["", "domingo", "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado"]
    for dia in dias_ordenados:
        if str(dia).upper() in weekdays:
            vetor.append(str(dia).upper())
    return vetor