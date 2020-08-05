# *-* coding: utf-8 *-*


from config import webhook_name, webhook_url
from webexteams_console_tools import webexconsole, getwebexRoomID
from webexteams import ValidaWebhook
from logica import logica, logica_pura
from webserver import run

import os

# Testa existencia do Webhook. Caso negativo, cria
# primeiro tenta variavies de ambiente, depois usa da config
msg=ValidaWebhook(os.getenv('WH_NAME',webhook_name),os.getenv('WH_URL',webhook_url))

# Imprime erro caso validacao do Webhook nao funcionou
if msg=="erro":
    print ("Erro de Webhook")


#Formato de execucao em modo console (teste)
formato = "w"

# Formato da conversa
# 0 = usuário constroi sua própria arvore de decisão
# 1 = usuário usa o mecanismo pronto de decisão (texto) ou via Cards
conversa = 1

if formato=="c":

    box=""

    # aviso
    print("exit para sair. help para comandos de usuario. help+ para comandos avançados")

    # a definicao do usermail (emai) e' importante para testar os filtros de usuario
    usermail=input("seu email>")


    # Para o caso de sala vazia no modo de console
    salaid=getwebexRoomID(input("nome da sala Webex:"))

    while box !="exit":

        box=input(">")

        # testa console de ferramentas
        webexconsole(box)
        
        # logica para usuarios
        
        if conversa==0:
            # usa arvo de decisao própria
            msg,arquivo=logica_pura(box,usermail)
            print (msg)
            print ("arquivo:"+str(arquivo))

        if conversa==1:
            # usa arvore de decisao pronta ou card
            msg,arquivo=logica(box,usermail,salaid)
            print (msg)
            print ("arquivo:"+str(arquivo))
        

elif formato=='w':
    
    run()

else:

    print ("nenhum formato selecionado. Selecione (c) para teste ou (w) para producao")
