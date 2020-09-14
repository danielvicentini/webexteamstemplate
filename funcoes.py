# -*- coding: utf-8 -*-


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

    
# Exemplo de função com 3 parametro
def tresparametros(parA,parB,parC):
    
    msg=f"Digitado: {parA} , {parB} e {parC}  \n"

    return msg

# Parte 2
# Trate aqui seus comandos
# identifique o que foi pedido pela variável codigo
# os parametros digitados estao em formato de lista na variável lista_parametros

def executa(usermail, codigo, lista_parametros):

    # deve retornar em formato de texto + arquivo com msg e arquivo

    # Variáveis que podem ser retornadas
    # MSG = O texto que é Obrigatório
    # Arquivo = Um arquivo que é anexado a mensagem no Teams
    # CARD = um Card do Webex no formato JSON (FUTURO)

    func=""
    #para msg
    msg=""
    #para arquivo
    arquivo=""
    # card (FUTURO)
    # card é um json
    

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

    elif codigo==40:
        # pega 2 parametros
        x=lista_parametros[0]
        y=lista_parametros[1]
        z=lista_parametros[2]
        func=tresparametros(x,y,z)
    
        
    # monta mensagem para retornar
    msg=msg+func
        
    return msg,arquivo

def executa_puro(comando, usermail):

    # usar esta funcão para definir sua própria lógica
    # retornar msg e arquivo para webex teams apresentar na mensagem

    msg=""
    arquivo=""

    msg=f"comando digitado: {comando}. Digitado por {usermail}"

    return msg,arquivo
