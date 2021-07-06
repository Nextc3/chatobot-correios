from urllib.request import urlopen 
from bs4 import BeautifulSoup


url = urlopen("https://www.correios.com.br/acesso-a-informacao/perguntas-frequentes") 

html = BeautifulSoup(url.read(),"html.parser")
perguntas = html.find_all("div", {"class": "accordion-titulo"})
respostas =  html.find_all("div", {"class": "panel"})
casa = [(i.strong).text for i in perguntas]
casa = "\n".join(casa)
print(casa)
'''
texto = {}
for i in range(20):
    texto[(perguntas[i].strong).text] = (respostas[i].p).text
   
texto.items()

'''
'''
    for p,r in perguntas, respostas:        
    pergunta =  (p.strong).text
    resposta = (r.p).text
    print(pergunta)
    print(resposta)

'''


