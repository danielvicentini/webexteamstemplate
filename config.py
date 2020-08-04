# -*- coding: utf-8 -*-

# Social main config file
# bot info
# admins info

import json

# Edit this
bot_language="BR"
# Insert Bot Token, Bot email, Bot Webhook Name and Bot Webhook URL
bottoken=""
botmail=""
webhook_name=""
webhook_url=""
admins="dvicenti@cisco.com"
admins_room="Nada"
bot_server_port=7000
    

# Novidade 27.4.20

#global vars
memoria={}



#------------------------------------------------------
#  Config Room
#------------------------------------------------------
#  Function that loads a config.json if desirable

def le_config():
    configuracao=dict()
    try:
        with open('config.json',encoding='utf-8') as json_file:
            configuracao=json.load(json_file)  
    except:
        pass
    return configuracao

# carrega  configuracoes, caso tenha
configuracao = le_config()

#---------------------------------------------------
# Bot options
#---------------------------------------------------
# Bot options
# bot structure
# { opcoes: [{
#		"tag": "<list of words to sugest>",
#		"title": "<option title>",
#		"desc": "<option description>",
#		"option": <integer code>,
#		"admin": <true or false, to be diplayed for admin users>,
#		"req": <true or false in case command requires parameters>,
#		"params": "<list of parameters comma separated"}
# },{ next option } ] }

# opçoes
# roadmap: 1) Arquivo JSON DONE, 2) GET/POST via http

# NOTA IMPORTANTE:
# O Arquivo json precisa ser salvo em UTF-8 e EOL deve ser Unix LF
# Usar o notepad++ para isto
# do contrário dará erro na leitura do arquivo no Unix

def le_options():
    # carrega opcoes do arquivo options.json
    try:
        with open('options.json',encoding='utf-8') as json_file:
            novas_opcoes=json.load(json_file)
    except:
        print ("erro na leitura do arquivo de opçoes")
    return novas_opcoes

# carrega opcoes da função
novas_opcoes=le_options()
