# -*- coding: utf-8 -*-

# This code was originaly Documented in Portuguese Language
# Daniel 6.26.2020

# admins & language
from config import admins, bot_language

# Bot config
from config import memoria, configuracao, novas_opcoes

# funcoes do projeto
from funcoes import executa, executa_puro

# Card & Buttons
from webexteamssdk.models.cards.inputs import Number, Text, Choices 
from webexteamssdk.models.cards.components import TextBlock, Choice
from webexteamssdk.models.cards.card import AdaptiveCard
from webexteamssdk.models.cards.actions import Submit


from webexteams import SendCard, getCardInputs,getCardInfo, getwebexRoomID

# ver 3.0 - 1.8.20
# ver 1.5 - 11.5.20

# Functions

#### FUNÇÕES A RESPEITO DAS OPÇÕES/COMANDOS DISPONÍVEIS AO USUÁRIO
#####################################################################

# Funcão para retornar menu com opções ao usuário
# Estas funções são chamadas dentro da logica

# Reads and presentes options to the user (from comando such as 'Help')

def opcoes_para_user_card(usermail,sala):

    global novas_opcoes
    
    # Ler options.json

    # definição de linguagem para o Card
    if bot_language=="BR":
        menu="Menu de Opções:"
        envia="Enviar"
        noe="Nenhum Opção Encontrada"
    else:
        menu="Available Options:"
        envia="Submit"
        noe="No Available Options"
     
    choices=list()

    try:
        # Le as opcoes de options conform admin ou não para montar opcoes
        for b in novas_opcoes['opcoes']:
            if usermail not in admins and b['admin']==True:
                # pula sessão se usuário não for admin
                continue
            else:
                choice_new=Choice(b['title'],str(b['option']))
                choices.append(choice_new)
    except:
        pass

    # monta Card
    greeting=TextBlock(menu,size="Medium",color="Light")
    body=[greeting]
    if len(choices)==0:
        # Coloca mensagem de 'Nenhuma Opção Encontrada" 
        body.append(TextBlock(noe))

        card= AdaptiveCard(body=body)

    else:
        escolhas=Choices(choices,"escolhas")
        body.append(escolhas)
        submit = Submit(title=envia,data={ "form":"menu"})

        #card = AdaptiveCard(body=[greeting,first_name,age], actions=[submit]) 
        card= AdaptiveCard(body=body, actions=[submit])

    # Envia a msg
    msg=SendCard(sala,card)
    if "erro" in msg:
        print("Erro no envio de card para a sala solicitada.")
    

    return msg

def funcao_card(option,sala):

    # envia um card específico conforme função
    
    #global configuracao

    if bot_language=="BR":
        envia="Enviar"
    
    else:
        envia="Submit"
        
     

    # resgata valores da opção pedida
    title=optparam(option, "title")
    if title!="":
        parametros=optparam(option, "req")
        desc=optparam(option,"desc")
        parametros=optparam(option, "req")
    else:
        # se chegou aqui nao encontrou dados com a opção informada
        return "erro"

    # Monta cabeçalho do card conforme a opção
    greeting=TextBlock(title,size="Medium",color="Light")
    greeting2=TextBlock(desc,size="Small",color="Accent")
    
    body=[greeting,greeting2]


    # Adiciona os campos de parâmetros conforme opção
    c=0
    if parametros==True:
        params=optparam(option,"params")
        lista=params.split(",")
        
        while c<len(lista):
            body.append(TextBlock(f"Digite o parametro para {lista[c]}:",size="Small"))
            body.append(Text(f"parametro{c}",placeholder=lista[c]))
            c+=1

    # identificador de funcao que é adicionado ao card, este identificador
    # dirá ao bot no POST seguinte para qual função estes parametros devem ir
    # os campos Parametros inditcam o total de parametros do form
    form={ "form":"function","option":option, "parametros":c}    

    submit = Submit(title=envia,data=form)
    

    #card = AdaptiveCard(body=[greeting,first_name,age], actions=[submit]) 
    card= AdaptiveCard(body=body,  actions=[submit])

    msg=SendCard(sala,card)
    if "erro" in msg:
        print("Erro no envio de card para a sala solicitada.")

    return msg



def opcoes_para_user(usermail):
    
    # acessa cada uma das opcoes da configuracao de opcoes
    # para apresentar a lista de comandos disponiveis ao user
    # esta condicionado a apresentar as opcoes se usuario for admin

    if bot_language=="BR":
        msg="***Comandos que eu entendo***:  \n\n"
    else:
        msg="***Commands that I understand***:  \n\n"
    
    z=1
    try:
        for b in novas_opcoes['opcoes']:
            if usermail not in admins and b['admin']==True:
                # pula sessão se usuário não for admin
                continue
            else:
                msg=msg+f"***{z}) {b['title']}***  \n"
                msg=msg+f"{b['desc']}  \n"
                z=z+1

        if bot_language=="BR":
            msg=msg+"  \nDigite algumas palavras para começarmos ou digite ***menucard*** para o modo card.  \n"
            
        else:         
            msg=msg+"  \nType keywords so we can start our chat or type ***menucard*** for card mode.  \n"
    except:

        if bot_language=="BR":
            msg="Nenhuma opção encontrada.  \n"    
        else:
            msg="No options found.  \n"

    return msg


# This function returns data from an specific user option

# Função que retorna dados a respeito de cada opção
# Ex: se requer parametros, quais as tags

def optparam(codigo,item):
    
    # investiga nas opcoes existentes para o user
    # devolve o valor do item conforme o codigo da opcao
    dado=""
    for b in novas_opcoes['opcoes']:
        try:
            if b['option']==codigo:
                try:
                    dado=b[item]
                except:
                    dado = "erro"
        except:
            dado="erro"    

    return dado

# This function try to understand the best match for an available option for the user based on keywords sent.

# Função que sugere melhor comando de acordo com o entendimento do usuário
# Entendimento é feito comparando o que o usuário escreveu com o valor da "tag" da opção    

def sugere_opcao(comando,usermail):

    global admins

    # recebe o comando, procura qual a melhor opcao mais proxima a este comando e devolve o código
    # update: analisa sugestões dependendo do usuário ser normal ou admin

    #variável para entencer qual a opcao da lista de comandos qu é mais parecido com o comando digitado
    score=0.0
    # loop para cada um das opções conhecidos
    # variavel c usada para procurar na lista de opcoes
    
    try:
        for b in novas_opcoes['opcoes']:

            if usermail not in admins and b['admin']==True:
                # pula sessão se usuário não for admin
                continue
            else:
                #
                txtnow=b['tag'].lower()
                opcao_cod=b['option']
                
                #variaveis
                # qtde de palavras no que foi digitado
                sp=comando.split(" ")
                y=len(sp)
                a=0
                found=0
                resultado=0.0
                
                # este laço conta a qtde de palavras que o comando digitado tem em comum com a opcao conhecida
                while a<y:
                    if sp[a] in txtnow:
                        found=found+1
                    a+=1

                # calcula o % de aproximacao do comando conhecido    
                resultado=found/len(txtnow.split(" "))
                
                # se tiver a melhor nota, vira provisoriamente a melhor opcao
                if resultado>score:
                    score=resultado
                    opescolhido=opcao_cod
                
                # Memoriza o comando escolhido como o mais proximo
                # somente se a nota for igual ou melhor que .3 
                # do contrario devolve 0 = nenhum
    except:
        # error in options
        pass

    if score>=.3:
        return opescolhido
    else:
        return 0

# Initiates memory for a user - used by the robot to chat with the user

# Função que inicia valores para um usuário conversando com o robo
# iniciar valores = convesarsa começando do zero.

def reinicia_user(usermail):
    
    global aguardando
    #global memoria
    #global configuracao
    
    # reinicia variavies da memoria par ao usuario
    # robo vai comecar do zero com este usuario
    try:
        var={ 'wait':False, 'option':0, 'req':False, 'params':False, 'typed':'','typing':False}
        memoria[usermail]=var
        aguardando=memoria[usermail]['wait']
    except:
        pass


### Main Code


#### PROGRAMA PRINCIPAL


### Step 0 - Ready options available from options.json
#################################################################

# 0) Inicio
# leitura do arquivo de opcoes


### Part 1 - Logic - main function - this function is called whenever a text arrives for the bot
#################################################################

# 1) logica
# É chamado a medida que um comando chega do usuário, seja via console (testes) ou via http (produção)

def logica(comando,usermail,salaid):

    # comando = o que user digitou
    # usermail = email do usuario
    # sala = roomId alvo - usado para as funções de Cards & Buttons

    global aguardando
    global memoria
    global configuracao

    # faz a logica de entender o comando pedido e a devida resposta para o usuario
    # o parametro usermail e' utilizado para identificar o usuario que solicitou o comando
    # Retorna mensagem para ser enviada para console ou Webex teams
    
    #Separa o comando por espacos
    #Primeiro item e'o comando em si, os demais sao parametros deste comando
    comando=comando.lower()
    sp=comando.split(" ")
        
    # 21.11.19
    # variavel arquivo para o caso do bot devolver arquivos anexados
    arquivo=""
    
    # no final, a função retorna o conteúdo de arquivo e msg = texto do robo
    msg=""
	
    # passo 1) recupera a conversa, caso ja tenha comecado
    # Do contrario entende que é uma conversa nova

    # entendendo se usuario já fez solicitacoes e o robo aguardo respostas
    # explicacao da memoria:
    # wait (true/false) = se robo esta esperando uma info do usuario
    # opcao = codigo do comando
    # req = se comando precisa de parametros
    # params = lista de parametros
    # para cada solicitacao do parceiro, esta logica atualiza estas variaveis



    try:
        # recupera o estado da memoria
        aguardando=memoria[usermail]['wait']
        
    except:
        # se chegamos aqui, usuario esta se comunicando pela primeira vez,
        # protanto variaveis serao criadas
        reinicia_user(usermail)
        aguardando=memoria[usermail]['wait']


        
    ### Part 2 - Start decision tree
    #################################################################

        
    # 2) Análise
    # Caso esteja no começa da conversa, este bloco entende o que o usuário quer fazer

    # 2.1 este bloco é para o caso do robo não saber ainda o que o user quer:
    if aguardando==False:
        
        # 2.1a. teste se user pediu ajuda
        if "help" in comando or "ajuda" in comando:
            # roda as opcaoes disponives
            # a reposta está condicionado ao user ser admin ou não
            msg=opcoes_para_user(usermail)
                
        #2.1b. tenta adivinhar o comando consultando os comandos disponiveis
        # caso ele encontre uma opcao, apresenta e apos isto o robo entra em modo de espera

        if msg=="" and len(sp)>0 and len(comando)>=5:
            # chama função que devolve o cod da opcao mais aproximada
            opescolhido=sugere_opcao(comando,usermail)
            if opescolhido != 0:
                # popula variaveis e pergunta se e' a escolhida
                memoria[usermail]['option']=opescolhido
                memoria[usermail]['wait']=True
                memoria[usermail]['req']=optparam(opescolhido,"req")
                if memoria[usermail]['req']==False:
                    # Se comando nao requer parametros, então ele está pronto para a logica de execucao
                    memoria[usermail]['params']=True
                else:
                    # Se o comando requer parametros, entao o prox passo é a logica de entrada de parametros
                    memoria[usermail]['params']=False

                if bot_language=="BR":
                    msg=f"Você quiz dizer: {optparam(opescolhido,'title')} ?  \n"
                else:
                    msg=f"Do you mean: {optparam(opescolhido,'title')} ?  \n"

                # Se chegou até aqui... na próxima interação robo fica a espera da continuidade da conversa
 
        # 2.1c nada conhecido, então devolve msg padrão

        if msg=="":
            if bot_language=="BR":
                msg="Olá. Digite ***ajuda*** para ver as opçoes disponíveis.  \nVou tentar adivinhar também o que você está procurando :-)  \n"
                msg=msg+"Novo: Digite ***menucard*** para ver no formato de card.  \n"
            else:
                msg="Hello. Type ***help*** to see available options.  \nI'll try to guess what you are looking for :-)  \n"
                msg=msg+"New: Type ***menucard*** to see in card mode.  \n"

   # Part 3
   # Robot expects information from user
   #################################################

    # 3) Conversando
    # Caso conversa já iniciado, usa este bloco

    # vai por este caminho se o robo espera resposta do usuario
    if aguardando==True:

        # resgata o código do comando em questão
        codigo=memoria[usermail]['option']
    
        # Textos padrão
        if bot_language=="BR":
            msg_titulo="Bem? Eu tinha entendido: ***"+optparam(memoria[usermail]['option'],'title')+"***.  \n"
            msg_sn="Diga ***sim*** ou ***ok*** para continuar ou digite ***não*** ou ***reinicie*** para recomeçarmos.  \n"
            msg_ready="Estou pronto para executar seu comando.  \n"
            msg_comma="Digite os parametros separados por virgulas. Você pode reiniciar digitando ***reinicie*** ou ***não***.  \n"
            msg_restart = "Ok, vou reiniciar nossa conversa.  \nDigite ***ajuda*** se quiser saber mais o que posso fazer."
            msg_ok="  \nEspero ter atendido sua expectativa.  \n"
            msg_empty="Não consegui executar devido a um erro na minha programação.  \n"
            
   
        else:
            # English
            msg_titulo=f"I understood ***{optparam(memoria[usermail]['option'],'title')}***.  \n"
            msg_sn="Type ***yes*** or ***ok*** to continue. Type ***no*** or ***restart*** to restart conversation.   \n"
            msg_ready="I'm ready to execute you command.  \n"
            msg_comma="Type your parameters separated by commas. You can also restart chat by typing ***restart*** or ***no***.  \n"
            msg_restart = "Ok, I'll restart our chat.  \nType ****help*** if you want to know what I can do."
            msg_ok="  \nI hope you've got what you asked.  \n"
            msg_empty="I couldn't find a way to execute what you asked me due to a failure in my code.  \n"
           

        # texto para
        # parametros necessários, caso precise
        if memoria[usermail]['req']==True:
            if bot_language=="BR":
                msg_need_params=f"Digite os parametros para completar o comando:***{optparam(memoria[usermail]['option'],'params')}***  \n\n"    
            else:
                # English
                msg_need_params=f"The following parameters are needed:***{optparam(memoria[usermail]['option'],'params')}***  \n\n"   


        # Se chegou até aqui, robo aguarda sim ou não para executar o comando
        if memoria[usermail]['params']==True:
            
            # resgata parametros caso comando precise deles
            if memoria[usermail]['req']==True:
                parametros=memoria[usermail]['typed']
                
                if bot_language=="BR":
                    msg_params=f"Voce digitou os parâmetros : ({parametros})  \n"
                else:
                    # English
                    msg_params=f"You typed: {parametros}  \n"
                            
            if "yes" in comando or 'ok' in comando or "sim" in comando:
            # se chegou aqui no Sim, vai executar se achar funcões para o código desejado
                
                if bot_language=="BR":
                    msg="Vou executar o que você me pediu:  \n\n"
                else:
                    # English
                    msg="Executing what you asked me:  \n\n"
                
                # Os parametros digitados estao na variavel do tipo lista abaixo
                lista_parametros=memoria[usermail]['typed'].split(",")
 
                #---------------------------------------------------------------------------------
                # INTERPRETAÇÃO DE CÓDIGOS AQUI
                # Suas funções estaram no módulo funções, que são chamados pela função executa(cod,lista de parametros)
                # codigo = codigo do comando
                # lista_parametros = lista com os parametros digitados pelo usuario, separado por virgulas
                # o resultado do seu código deve ser atribuido a variavel msg

                #trata os comandos conforme necessidade do projeto
                resultado=""                            
                resultado,arquivo=executa(codigo,lista_parametros)
                
                if resultado=="":
                    # Devolveu resultado vazio - provavelmente porque funcao nao retornou nada ou erro no código
                    msg=msg+msg_empty

                # uma vez que serviço entregue, zera a memória da conversa
                reinicia_user(usermail) 

                # monta mensagem final para user após execução do comando
                msg=msg+resultado+msg_ok
                

            else:

                # caso ainda não tenha digitado o sim, então pede o prox passo:

                # mensagem do robo caso comando requer parametros
                if memoria[usermail]['req']==True:
                    msg=msg_titulo+msg_params+msg_ready+msg_sn
                else:
                # mensagem do robo caso comando nao requer parametros
                    msg=msg_titulo+msg_ready+msg_sn
                
        # se chegou aqui, aguarda parametros, mas ainda não estão prontos
        elif memoria[usermail]['params']==False:
            
            if memoria[usermail]['typing']==True:


                # fica neste modo a espera dos parametros
                # quando qtde de comandos está ok, define que qtde de parametros esta correta
                                    
                #copia ultimo comando para memoria
                memoria[usermail]['typed']=comando
                parametros=memoria[usermail]['typed']
                
                # testa se qtde de comandos está ok
                # lista de comandos que se espera
                parametros_esperados=(optparam(memoria[usermail]['option'],"params").split(","))
                # lista de comandos digitadaos
                parametros_digitados=(parametros.split(","))
                
                # testa se qtde de comandos está ok
                if len(parametros_esperados) == len(parametros_digitados):
                    texto=""
                    c=0
                    while c<len(parametros_digitados):
                        texto=texto+parametros_esperados[c]+"="+parametros_digitados[c]+" "
                        c+=1
                    
                    # Se chegou até aqui, avisa agora que falta só o sim
                    msg=msg_titulo
                    if bot_language=="BR":
                        msg_typed=f"você digitou: {texto}  \n"
                    else:
                        msg_typed=f"You typed: {texto}  \n"
                    msg=msg+msg_typed
                    msg=msg+msg_sn
                    memoria[usermail]['params']=True
                else:
                    msg=msg_titulo+msg_need_params+msg_comma


               # se chegou aqui, aguarda user dizer se é o comando inicialmente está correto ou não
            else:

                if 'yes' in comando or 'ok' in comando or 'sim' in comando:
                    msg=msg_need_params
                    msg=msg+msg_comma
                    memoria[usermail]['typing']=True
                    # sendo sim, significa agora que está a espera de parametros
                else:
                    msg=msg_titulo+msg_sn

        # 4 - User cancelled conversation
        ##############################################

        # 4)  Usuário cancelou a conversa  então este bloco recomeça

        # Reinicia conversa se usuario pedir
        if 'restart' in comando or "no" in comando or "não" in comando or "reinicia" in comando:
            msg=msg_restart
            reinicia_user(usermail)

    # comandos de teste
    
    if 'memoria' in comando:
        
        #resgata a memoria
        #caso falhe, sinal de que nao ha memoria
        try:
            msg="cógigo:"+str(memoria[usermail]['option'])
            msg=msg+"  \nwait:"+str(memoria[usermail]['wait'])
            msg=msg+"  \nrequer parametros:"+str(memoria[usermail]['req'])
            msg=msg+"  \nparametros:"+str(memoria[usermail]['params'])
            msg=msg+"  \ndigitando parametros:"+str(memoria[usermail]['typing'])
            msg=msg+"  \no que foi digitado:"+str(memoria[usermail]['typed'])
        except:
            msg="Erro no resgate da memoria"    


    #### NESTE TRECHO FUNCOES COM CARDS & BUTTONS

    # monitorar resultado do chamado dos cards
    
    result=""
    
    # chama o card de opções
    if comando=="menucard":
        result=opcoes_para_user_card(usermail,salaid)

    # chama um card específico
    # o comando completo deve ser showcard:xy onde xy representa o codigo da opção
    if "showcard" in comando:
        try:
            cartao=comando.split(":")
            result=funcao_card(int(cartao[1]),salaid)
        except:
            result="erro"


    if result=="erro":
        if bot_language=="BR":
            msg_erro="Não pude enviar Cartão."
        else:
            msg_erro="Could't send card to you."

        # Se chegou até aqui ajuda ou envio de cartão falhou
        msg=msg_erro


    if result=="ok":
        # se ok é porque um card foi enviado
        if bot_language=="BR":
            msg_card="Enviei um card para você.  \n"
        else:
            msg_card="I sent a card to you.  \n"
        msg=msg_card



    return msg,arquivo



def logica_pura(comando,usermail):
   
    # Usar este modelo para casos de contruir uma logica nova
    
    #Separa o comando por espacos
    #Primeiro item e'o comando em si, os demais sao parametros deste comando
    comando=comando.lower()
    
        
    # 21.11.19
    # variavel arquivo para o caso do bot devolver arquivos anexados
    arquivo=""
    
    # no final, a função retorna o conteúdo de arquivo e msg = texto do robo
    msg=""
	
    msg,arquivo=executa_puro(comando, usermail)

    return msg,arquivo
