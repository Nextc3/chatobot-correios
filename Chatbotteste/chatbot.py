
#olá
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

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
    "Olá, tudo bem? Como você está?", 
    "Estou bem, e com vc?",
    "Também estou bem. Em que posso te ajudar?",
    "Estou em dúvida em namorar entre duas pessoas",
    "Sério?",
    "Sim...", 
    "Você é não monogâmico?",
    "Sou, mas elas não são",
    "Você sabe que é difícil se relacionar com monogâmicos, não é?",
    "Sei sim",
    "Então... vai insistir com essas escolhas?",
    "Vou"
    ])
while True:
    try:
        resposta = bot.get_response(input("Você: "))
        if float(resposta.confidence) > 0.2:
            print("Carteirin: ", resposta)
        else:
            print("Não manjo dessas paradas :(")
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
