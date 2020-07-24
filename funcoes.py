# -*- coding: utf-8 -*-

# arquivo de funcões customizadas de acordo com o que se queira fazer pelo bot
# 
# Este é o arquivo de trabalho do seu robo
# Ele é divido em duas partes
# 1) Suas funcoes customizadas para chamar outras aplicacoes e executar suas atividades
# 2) As funçõe do item 1 são chamadas conforme o código da opção identificado


# imports
import json

# custom comands function for this bot
from config import le_config

# Parte 1
# Defina aqui suas funções

# Exemplo de função sem parametros
def semparametros():

    msg="Olá. Exemplo de função sem parametros.  \n"

    return msg

# Exemplo de função com 1 parametro
def umparametro(parametro):

    msg=f"Digitado: {parametro}  \n"

    return msg


# Exemplo de função com 2 parametro
def doisparametros(parA,parB):
    
    msg=f"Digitado: {parA} e {parB}  \n"

    return msg

# Trate aqui seus comandos
# identifique o que foi pedido pela variável codigo
# os parametros digitados estao em formato de lista na variável lista_parametros

def executa(codigo, lista_parametros):

    # deve retornar em formato de texto + arquivo com msg e arquivo

    # Variáveis que podem ser retornadas
    # MSG = O texto que é Obrigatório
    # Arquivo = Um arquivo que é anexado a mensagem no Teams
    # CARD = um Card do Webex no formato JSON (FUTURO)

    #para msg
    msg=""
    #para arquivo
    arquivo=""
    # card (FUTURO)
    # card é um json
    card=""

    # a Partir daqui trata suas funções conforme código

    if codigo==10:
        # função sem parâmetro
        func=semparametros()
        
    elif codigo==20:
        # pega o parametro 1
        x=lista_parametros[0]
        func=umparametro(x)
        
    elif codigo==30:
        # pega 2 parametros
        x=lista_parametros[0]
        y=lista_parametros[1]
        func=doisparametros(x,y)
        
    # monta mensagem para retornar
    msg=msg+func
        
    return msg,arquivo,card
