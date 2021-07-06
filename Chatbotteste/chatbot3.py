'''
INF032 - T05
Caio Costa e Camila Marinho

Referências e bibliotecas usadas:
https://chatterbot.readthedocs.io/en/stable/
https://escoladeia.com.br/construindo-um-chatbot-em-10-minutos-no-python/
https://pypi.org/project/pyrastreio/
https://pypi.org/project/Consulta-Correios/
https://pypi.org/project/pycep-correios/
https://medium.com/@lucaaslb/web-scraping-com-python-ada1f5e3f921
'''

import random, os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from pyrastreio import correios
import consulta_correios
from requests.sessions import TooManyRedirects
from pycep_correios import get_address_from_cep, WebService
from urllib.request import urlopen 
from bs4 import BeautifulSoup
from bs4.element import ResultSet

def getPerguntas(html):
    return html.find_all("div", {"class": "accordion-titulo"})

def getRespostas (html):
    return html.find_all("div", {"class": "panel"}) 

def getPergunta (perguntas,i):
    return (perguntas[i].strong).text

def getResposta (respostas,i):
    return (respostas[i].p).text

def soPerguntas(perguntas):
    return [(i.strong).text for i in perguntas]

def processarMenu(opcao, nome):
    os.system('cls||clear')
    if (opcao == 1):
        consultaStatus(nome)
    elif (opcao == 2):
        consultaCEP(nome)
    elif (opcao == 3):
        consultaReclamacao(nome)
    elif (opcao == 4):
        consultaFrequentes()
    elif (opcao == 5):
        iniciaChatbot(nome)

def consultaStatus(nome):
    numeroRastreio = input('{}, digite o número de rastreio: (exemplo: NX077755161BR) '.format(nome))
    encomenda = correios(numeroRastreio)
    if (len(encomenda) != 0):
        ultimoStatus = correios(numeroRastreio)[0]
        print('Data/Hora: {}/{}, Local: {}, Status: {}.'.format(ultimoStatus['data'],ultimoStatus['hora'],ultimoStatus['local'],ultimoStatus['mensagem']))
    else:
        print ('Objeto não encontrado.')

def consultaCEP(nome):
    cep = input('{}, digite o CEP: (Exemplo: 13076-001) '.format(nome))
    try:
            resultado = consulta_correios.busca_cep(cep)
            if(type(resultado) is dict):
                print(resultado['error'])
            else:
                endereco = resultado[0]
                print('Endereço: {}, Bairro: {}, Cidade/Estado: {}.'.format(endereco['address'],endereco['neighborhood'],endereco['city/state'])) 
    except(TooManyRedirects):
            print('Buscando alternativa de cep')
            address = get_address_from_cep(cep, webservice=WebService.VIACEP)
            print('Logradouro: {}, Bairro: {}, Cidade: {}, Estado: {}.'.format(address['logradouro'],address["bairro"],address['cidade'], address["uf"]))

#dicionário das reclamações
dict_reclamacoes = {
    1: [{'data/hora': '09/04/2021 09:55', 'andamento': 'Reclamacao cadastrada', 'status': 'Aberta'},
    {'data/hora': '30/04/2021 10:27', 'andamento': 'Solicitação de intervenção da Ouvidoria', 'status': 'Em tratamento'}],
    2: [{'data/hora': '28/05/2021 09:14', 'andamento': 'Reclamacao cadastrada', 'status': 'Aberta'}],
    3: [{'data/hora': '15/05/2021 11:55', 'andamento': 'Reclamacao cadastrada', 'status': 'Aberta'},
    {'data/hora': '30/05/2021 10:27', 'andamento': 'Em análise', 'status': 'Em tratamento'},
    {'data/hora': '10/06/2021 14:15', 'andamento': 'Respondida ao usuário', 'status': 'Concluída'}],
}
def consultaReclamacao(nome):
    reclamacao = int(input('{}, digite o código da manifestação: (Exemplo: 1) '.format(nome)))
    if (reclamacao in dict_reclamacoes.keys()):
        for status in dict_reclamacoes[reclamacao]:
            print('Data/Hora: {}, Andamento: {}, Status: {}.'.format(status['data/hora'],status['andamento'],status['status']))
    else:
        print('Reclamação não encontrada.')

url = urlopen("https://www.correios.com.br/acesso-a-informacao/perguntas-frequentes") 
html = BeautifulSoup(url.read(),"html.parser")
#dicionario com as respostas das perguntas frequentes
dict_perguntasfrequentes = {x+1: getResposta(getRespostas(html),x) for x in range(20)}
def consultaFrequentes():
    #Mostra as perguntas
    print("Perguntas Frequentes:")
    for i in range(20):
        print(getPergunta(getPerguntas(html),i))
    
    while True:
        try:
            print('\n')
            pergunta = int(input('Digite o número da pergunta ou acione CTRL+c para voltar ao menu anterior: '))
            print(dict_perguntasfrequentes[pergunta])
        except(KeyboardInterrupt, EOFError, SystemExit):
            os.system('cls||clear')
            break
    
def iniciaChatbot(nome):
    #cria bot Carteirin
    bot = ChatBot(
        'Carteirin',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///interacao.sqlite3', #banco para salvar as interacoes pra refinar a conversa
        logic_adapters=['chatterbot.logic.BestMatch'] #logica para o bot achar o melhor match para a pergunta feita
    )

    conversa = ChatterBotCorpusTrainer(bot)
    conversa.train('chatterbot.corpus.portuguese')
    conversa = ListTrainer(bot)

    protocolo = random.randint(10000,99999)
    listaConversa = [
        'Qual o seu nome?',
        'Carteirin, seu atendente virtual dos Correios do Brasil. Qual é seu nome?',
        'Meu nome é {}.'.format(nome),
        'Em que posso te ajudar, {}?'.format(nome),
        'Prazer em te conhecer.',
        'Rastrear objeto extraviado.',
        'Mas {}, você pode consultar o status do objeto no menu anterior na opção 1.'.format(nome),
        'Consultar CEP ou endereço',
        'Mas {}, você pode consultar o CEP no menu anterior na opção 2.'.format(nome),
        'Consultar reclamação.',
        'Mas {}, você pode consultar o status da reclamação menu anterior na opção 3.'.format(nome),
        'Não resolveu meu problema.',
        'Sinto muito. Eu sei como é chato não conseguir resolver algo. Deseja abrir uma reclamação, {}?'.format(nome),
        'Sim. Qual o protocolo?'
        'Anote o protocolo {}.'.format(protocolo),
        'Quero acionar a Ouvidoria.',
        '{}, para acionar a Ouvidoria ligue gratuitamente para 0800 722 7234 (atendimento em dias úteis, das 8h às 20h). Posso te ajudar em mais alguma coisa?'.format(nome),
        'Sim',
        'Pode falar {}. Estou aqui para te ajudar'.format(nome),
        'Fale sobre os Correios',
        'Empresa Brasileira de Correios e Telégrafos (ECT), ou simplesmente Correios, é uma empresa pública federal responsável pela execução do sistema de envio\n e entrega de correspondências no Brasil, mas que não se limita a apenas essa atividade:\n executa a distribuição de encomendas em todo o território nacional,\n bem com presta outros serviços de apoio ao Governo - em todas as esferas\n - e de apoio à população. O que você mais deseja?'
        'Quem é o presidente?',
        'O atual presidente dos Correios é Floriano Peixoto Vieira Neto',
        'Qual é lema dos Correios?',
        'O lema dos Correio é Soluções que aproximam',
        'Onde fica a sede dos correios?',
        'Brasília, Brasil.',
        'Quem é presidente do Brasil?',
        'Jair Messias Bolsonaro',
        'Conte história sobre os correios',
        'Os Correios tiveram sua origem no Brasil em 25 de janeiro de 1663,\n com a criação do Correio-Mor\n no Rio de Janeiro, embora a capital da colônia fosse então Salvador. Em 1931 o decreto 20 859, de 26 de dezembro de 1931\n funde a Diretoria Geral\n dos Correios com a Repartição Geral dos Telégrafos e cria o Departamento dos Correios e Telégrafos.\n A ECT foi criada a 20 de\n março de 1969, como empresa pública vinculada ao\n Ministério das Comunicações mediante a transformação da autarquia\n federal que era, então, Departamento de Correios e Telégrafos (DCT). A mudança não representou\n apenas uma troca de sigla, foi seguida por uma transformação profunda\n no modelo de gestão do setor postal brasileiro, tornando-o mais eficiente',
        'conte uma piada',
        'Se o PAC-MAN corresse como o Sonic, o jogo se chamaria SEDEX-MAN.',
        'Qual o nome completo dos correios?',
        'Empresa Brasileira de Correios e Telégrafos',
        'Quando os correios foram fundados?',
        'Como Correio-Mor: 25 de janeiro de 1663 (358 anos) e como Empresa de Correios e Telégrafos: 20 de março de 1969 (52 anos)',
        'Qual tipo de empresa os correios é?',
        'Empresa Brasileira de Correios e Telégrafos',
        'Privatizar os correios',
        'Os Correios é do povo e nunca deverá ser privatizado. Lutaremos até o fim para manter como empresa estatal']

    url = urlopen("https://www.correios.com.br/acesso-a-informacao/perguntas-frequentes") 
    html = BeautifulSoup(url.read(),"html.parser")

    for i in range(20):
        #Caso a pessoa digite a pergunta toda, o chatbot responder-la
        listaConversa.append(getPergunta(getPerguntas(html),i))
        listaConversa.append(getResposta(getRespostas(html),i))
        #Abaixo supõe que o usuário só digite um referente a pergunta feita
        #Adiciona uma pergunta e uma resposta como nome
        listaConversa.append(getPergunta(getPerguntas(html),i))
        listaConversa.append(str(i + 1))
        listaConversa.append(getResposta(getRespostas(html),i))
    
    conversa.train(listaConversa)
    
    print('Chat iniciado.')
    print('''Carteirin: Olá, tudo bem? Meu nome é Carteirin.
    Sou seu amigo e te ajudarei a resolver seu(s) problema(s) com os Correios - Empresa Brasileira de Correios e Telégrafos do Brasil.
    Qual é seu problema?
    (Para voltar ao menu anterior acione Ctrl+c.)''')

    while True:
        try:
            resposta = bot.get_response(input('Você: '))
            if float(resposta.confidence) > 0.2: #grau de confiança da resposta for maior que 0.2
                print('Carteirin:', resposta)
            else:
                print('Desculpa. Não entendi. Pode ser mais claro, por favor?')
        except(KeyboardInterrupt, EOFError, SystemExit):
            print('Chat finalizado.')
            os.system('cls||clear')
            break

print('Bem vindo ao atendimento dos Correios!')
nome = input('Qual seu nome? ')
print('\n')

while True:
    print('Em que posso ajudar, {}?'.format(nome))
    print('[1] Consultar status de encomenda.')
    print('[2] Consultar CEP.')
    print('[3] Consulta status de reclamação.')
    print('[4] Perguntas frequentes.')
    print('[5] Falar com atendente virtual.')
    print('[0] Sair do sistema.')
    
    resposta = int(input('Digite opção do menu: '))
    if (resposta == 0):
        print('Fim de atendimento.')
        break
    if (resposta > 0 and resposta <= 5):
        processarMenu(resposta, nome)
    else:
        print ('Opção de menu inválida.')
    print('\n')