def filtrosSelecionados(dicionario):
    queryParametrosSelecionados = ""
    for chave in dicionario:
        if dicionario[chave] != "":
            queryParametrosSelecionados += f" AND {chave} = '{dicionario[chave]}'"
    return queryParametrosSelecionados

def parteSelects(dictDescricaoParametros):
    querySelects = ""
    for chave in dictDescricaoParametros:
        tabela = dictDescricaoParametros[chave]["tabelas"][-1]
        coluna = dictDescricaoParametros[chave]["coluna"]
        querySelects += f"{tabela}.{coluna} as {chave},"
    querySelects = querySelects[:-1]
    return querySelects

def parteJoins(dictDescricaoParametros):
    queryJoins = ""
    for chave in dictDescricaoParametros:
        tabelas = dictDescricaoParametros[chave]["tabelas"]
        for i in range(len(tabelas)):
            if i == 0:
                strInserir = f""" INNER JOIN {tabelas[i]} ON segundoregistrado.Id{tabelas[i]} = {tabelas[i]}.Id"""
            else:
                strInserir = f""" INNER JOIN {tabelas[i]} ON {tabelas[i-1]}.Id{tabelas[i]} = {tabelas[i]}.Id"""
            if not queryJoins.__contains__(strInserir):
                queryJoins += strInserir
    return queryJoins

def tabelaCompletaJoinFiltros(dicionario, dictDescricaoParametros):
    completaQuery = ""
    for chave in dicionario:
        if dicionario[chave] != "":
            tabelas = dictDescricaoParametros[chave]["tabelas"]
            for i in range(len(tabelas)):
                if i == 0:
                    strInserir = f""" INNER JOIN {tabelas[i]} ON sreg.Id{tabelas[i]} = {tabelas[i]}.Id"""
                else:
                    strInserir = f""" INNER JOIN {tabelas[i]} ON {tabelas[i-1]}.Id{tabelas[i]} = {tabelas[i]}.Id"""

                #Faz a junção das tabelas apenas se não tiver sido feita ainda
                if not completaQuery.__contains__(strInserir):
                    completaQuery += strInserir
            completaQuery += f" AND {tabelas[-1]}.{dictDescricaoParametros[chave]['coluna']} = '{dicionario[chave]}'"
    return completaQuery  
