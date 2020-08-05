# Webex Teams Template 3.0

Modelo para criação do seu bot Webex Teams.

## Características

* Pronto para rodar em PaaS ou IaaS
* Implantação Rápida: basta definir os comandos que o Bot vai entender
* Reduzido tempo para protótipo de produção
* Interface com usuário em Portugues ou Ingles
* Conversar em formato de passos ou por meio de formulário (Cards).

## Funcionalidades

* Mecanismo de arvore de decisão para convesar com o usuário e entender o comando pedido
* Mecanismo de formulário (Cars) para acelerar os pedidos dos usuários
* Suporta comandos para usuários do tipo adminsitrador e usuário comum
* Suporta a construção rápida dos comandos através de arquivo JSON
* Pronto para pedir os parâmetros do comando
* Devolve código do comando e os parâmetros digitados para o desenvolvedor construir imediatamente suas funções para seu projeto
* Permite rodar em modelo de teste local (linha de comando) antes da produção
* Infraestrutura Web pronta para receber Webhook e POSTS integrada

## Instalação

### Pré-requisitos

* Definir local de implantantação do bot (Plataforma PaaS, IaaS, etc)
* Definir URL do Bot
* Token e email do Bot Webex Teams
* Definir 1 palavra chave para Webhooks

### Passos para Instalação

* Fazer o clone deste projeto
* Apontar os parâmetros do Robo. Opções:
* Opção 1: Editar o arquivo *config.py* com os 4 parametros necessários: Token, Email, URL e idenfiticado do Webhook
* Opção 2: Criar os 4 parametros como variáveis de ambiente com os seguintes nomes:
* WH_NAME = identificado ro webhook
* WH_URL = endereço e porta da URL onde o bot ficará hospedado (porta default é 80)
* BOT_MAIL = endereço de email do bot
* BOT_TOKEN = Token do Bot
* Opcional: O Robô fornece informações em português ou ingles. Defina esta opção na variável *bot_language* no arquivo *config.py*. Use BR para português. Qualquer outro conjunto de letras será usado Inglês.

### Opções para o usuário

O robô usará um arquivo de opções para apresentá-las ao usuário. Esta informação está no arquivo *options.json*.

Edite este arquivo conforme o interesse do seu projeto.

Identificação das opções:
* option: identificador único do comando - este valor será utilizado para executar as funções que vc irá criar
* tag: conjunto de palavras que o robô vai usar para tentar adivinhar o que o usuário escreve
* title: O título do comando que será apresentado para o usuário
* desc:  Descrição detalhada do comando
* req: Falso ou Verdade para identificar se o comando requer ou não parâmetros
* params: lista de parâmetros requeridos ao comando separados por vírgula.
* admin: Falso ou Verdade se este comando é ou não um comando exclusivo para administradores

### Informações adicionais

### Administrador do Bot

O robô diferencia administradores de usuários comuns, caso certos comandos precisem desta organização.

Para identificar quais são os administradores, coloque endereços de email separados por vígula na variável *admins* no arquivo *config.py*

O robô também tem um mecanismo para enviar mensagems para uma sala de administradores. Para isto defina o nome da sala dos admins na variável *admins_room* no arquivo *config.py*.
 
### Uso

Abrir uma sala 1:1 com o seu bot. Perguntar por **Ajuda** ou **Help**. O robô apresentará as opções disponíveis no arquivo *options.json* caso o usuário tenha direito a ele.

O robô irá perguntar baseado no que foi pedido pelo usuário o comando mais aproximado, caso o usuário confirme, o robô passará a pedir os parâmetros para executar esta função.

Caso o usuário deseje utilizar o modelo de formulários (Cards) ele pode optar por este modelo rodando o comando **menucard**. O Robô passará a apresentar as alternativas e pedir os parâmetros de função usando os Cards.

### Funcões a serem criadas conforme seu projeto

Após seleção da opções e parâmetros, o robô executará a função específica conforme seu identificador único . Seu trabalho será popular o arquivo *funcoes.py* para executar suas funções. A função *executa(codigo, lista_de_parametros)* é a responsável em receber os dados e executar as funções.

### Exemplo: função simples que devolve um informação

Neste exemplo, o robô tem 1 função de apresentar o parâmetro que você digitou. A opção tem o código 10 e aceita 1 parâmetro. Logo a função a ser escrita pode ser:

def executa(codigo,lista_de_parametros):

 if codigo=10:
 
     #pega o primeiro parametro informado
     
     parametroDigitado=lista_de_parametros[0]
     
     msg=f"Você digitou {parametroDigitado}"
     

     return msg

Obrigatoriamente o robô devolve ao usuário o resultado escrito na variável *msg*.

### Testando o projeto

Antes de entrar em produção, é possível rodar o código localmente em modo de texto (console) para testar suas funções.

Para tanto, editar o arquivo *meubot.py* e editar a variável **formato="c"**. Neste modelo o robô não levantará o servidor Web para receber Webhooks, mas pode ser usado para testar suas funções. O programa perguntar um usermail para identificar o usuário e 1 sala Webex Teams para testes.

Para sair do modo console, digite **Exit**.

### Rodando o projeto

Rodar o bot chamando o código principal *meubot.py*

### Colocando em Produção

Editar o arquivo *meubot.py* e editar a variável **formato="w"**. Neste modelo o robô levanta o servidor Web e fica no aguardo dos webhooks dos usuários.



Feito em Pyton 3.7.2

Daniel Vicentini
Atualizado em 05 de agosto de 2020

v2.24 de julho de 2020
