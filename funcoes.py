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


def executa_card(comando,usermail):

    # a ser removido, nao faz mais sentido já que logica cuida do card
    # e execução final é a mesma função executa acima.
    
    msg=""
    arquivo=""

    
    """ 
    # usar esta funcão para definir sua própria lógica de envio dos cards
    # retornar msg e arquivo para webex teams apresentar na mensagem
    
    
    if "ajuda" in comando:

        # le options.json e monta um card de opçoes
        
        novas_opcoes=le_options()
        # Ler options.json

        
        greeting=TextBlock("Menu de Opçoes",size="Medium",color="Light")
        body=[greeting]

        #op= { "opa":"1"}
        #opcoes=list()
        #opcoes.append(op)
        
        choices=list()
        #choice1=Choice("sim",1)
        #choices.append(choice1)
     
        #choice2=Choice("no","no")
        #choices.append(choice2)
        
        for b in novas_opcoes['opcoes']:
            # valor da opção, mesmo que inteiro precisa estar em formato string
            choice_new=Choice(b['title'],str(b['option']))
            choices.append(choice_new)
           

        escolhas=Choices(choices,"escolhas")

        body.append(escolhas)

        submit = Submit(title="Enviar")

    
        #card = AdaptiveCard(body=[greeting,first_name,age], actions=[submit]) 
        card= AdaptiveCard(body=body, actions=[submit])
        sala=input ("nome da sala:")
        msg=SendCard(sala,card)
        if "erro" in msg:
            msg="Erro no envio de card para a sala solicitada."



        #lista=opcoes.split(",")
        #    print (lista)
        #    c=0
        #    while c<len(lista):
        #        body.append(Choices(id=list[c],(f"Digite o parametro para {lista[c]}:",size="Small"))
        #        body.append(Text(f"parametro{c}",placeholder=lista[c]))
        #        c+=1
            
    if "get" in comando:

        # função para pegar dados enviado a um card

        id="Y2lzY29zcGFyazovL3VzL0FUVEFDSE1FTlRfQUNUSU9OL2M4NzAwNmMwLWQzNTQtMTFlYS1hOTk0LWY5NDNjNmNlODQzYw"
        content=getCardContent(id)
        z=json.loads(json.dumps(content.inputs))
        
        print (z['option'])
        print (z['parametros'])
        y=int(z['parametros'])
        b=0
        while b<y:
            chave="parametro"+str(b)
            print (f"Parametro {b}:{z[chave]}")
            b=b+1
        

    if "card" in comando:

        opcao="30"
        desc="Descrição da opção"
        parametros=True
        params="Nome da sala,Qtde de pessoas na sala"
        
        # Monta cabeçalho do card conforme a opção
        greeting=TextBlock(opcao,size="Medium",color="Light")
        greeting2=TextBlock(desc,size="Small",color="Accent")
        
        body=[greeting,greeting2]


        # Adiciona os campos de parâmetros conforme opção
        c=0
        if parametros==True:
            lista=params.split(",")
            
            while c<len(lista):
                body.append(TextBlock(f"Digite o parametro para {lista[c]}:",size="Small"))
                body.append(Text(f"parametro{c}",placeholder=lista[c]))
                c+=1

        # identificador de funcao que é adicionado ao card, este identificador
        # dirá ao bot no POST seguinte para qual função estes parametros devem ir
        # os campos Parametros inditcam o total de parametros do form
        form={ "option":opcao, "parametros":c}    

        #text=Text("text",placeholder='text',maxLength=5, height="10px")
        #first_name=Text('first_name', placeholder="Digite seu nome")
        #age = Number('age', placeholder="Digite sua Idade")
        submit = Submit(title="Enviar",data=form)
        
    
        #card = AdaptiveCard(body=[greeting,first_name,age], actions=[submit]) 
        card= AdaptiveCard(body=body,  actions=[submit])

        sala=input ("nome da sala:")
        msg=SendCard(sala,card)
        if "erro" in msg:
            msg="Erro no envio de card para a sala solicitada."
    """
    return msg,arquivo