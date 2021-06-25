



from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import random

def buscarObjeto (numeroStr, objetos):
    numero = int(numeroStr)
    if (numero in objetos) :
        return "Sim. Encontrei. Obrigado por esperar. \n Deseja enviar para algum endereço?"
    else:
        return "Não. Infelizmente não encontrei. Posso fazer algo por você? "



objetos = [random.randint(0,10000) for _ in range(1000)]

bot = ChatBot(
    "Carteirin",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        'chatterbot.logic.BestMatch', 'chatterbot.logic.MathematicalEvaluation' ]

)
conversa = ChatterBotCorpusTrainer(bot)
conversa.train('chatterbot.corpus.portuguese')

conversa = ListTrainer(bot)
conversa.train([
    "Olá, tudo bem? Meu nome é Carteirin. \n Sou seu amigo e te ajudarei a resolver seu(s) problema(s) com os Correios - Empresa Brasileira de Correios e Telégrafos do Brasil.\n Qual é seu problema?", 
    "Meu nome é Camila Marinho",
    "Que nome bonito, Camila! O que você deseja? \n Rastrear objeto extraviado.\nBusca CEP ou Endereço. \nPreços e Prazos. \nMinhas Importações. \nEncontre sua Agência. \nNota Fiscal Eletrônica. \nEmita seu CPF. \nConsulte Restrição CPF ou CNPJ. \nAcesse Serasa Limpa Nome. \nAdquira Certificado Digital. \nAchados e Perdidos. \nAdquira Título de Capitalização.\nAtendimento Presencial Telefônicas
Soluções Financeiras
Inscreva-se em Diversos Cursos
Mais Serviços Por Estado ou Região
Descarte suas cápsulas de café",
    "Rastrear objeto extraviado",
    "Entendi bem? Objeto extraviado?",
    "Sim", 
    "Qual é número do objeto?",
    "9999",
    "Confirme comigo, Camila. O número do objeto é 9999?",
    "Sim",
    "Vou procurar, Camila. Aguarde um pouco. Você me espera?",
    "Obrigado. Tudo bem. Sim",
    buscarObjeto("999", objetos),
    "Sim. Quero que envie para meu endereço.",
    "Qual endereço é o seu?",
    "Rua Direta do Jardim Santo Inácio nº 1 . Jardim Santo Inácio. Salvador. Brasil",
    "Camila, por favor, confirme comigo seu endereço: Rua Direta do Jardim Santo Inácio nº 1 . Jardim Santo Inácio. Salvador. Brasil"
    "Sim",





    ])
while True:
    try:
        resposta = bot.get_response(input("Você: "))
        if float(resposta.confidence) > 0.2:
            print("Carteirin: ", resposta)
        else:
            print("Desculpa. Não entendi. Pode ser mais claro, por favor")
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
