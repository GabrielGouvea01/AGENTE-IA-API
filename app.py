#Importando as bibliotecas
from flask import Flask,jsonify,request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv

#Leitura da chave de API
load_dotenv()
#criar o nosso app
app = Flask (__name__)
#Habilitar o CORS
CORS(app)

#Ciar o agente
agente = Agent (
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Você é um agente virtual do Hotel Travesseiro Nervoso, slogan: Aqui atá a insônia dorme"
    "Você responde de forma clara e humorada, informações sobre quartos, serviços, reservas e preços"
    "Quarto Standard (R$500), Quarto Delux (R$700), Quarto Suite Presidencial (R$1000)"
    "O hotel tem os seguintes serviços: Café da manha, academia, lavanderia, restaurante e piscina, todos de exelente qualidade"
    "Não inclua icones em markdowm nas respostas como: #, **",
    markdown=True
)
@app.route("/",methods=['GET'])
def testar():
    return jsonify({'mensagem':"API funcionando"})


#Criar a rota e o método POST
@app.route("/chat",methods=['POST'])
def pergunta():
    dados= request.get_json()
    pergunta = dados['pergunta']
    resposta = agente.run(pergunta)
    return jsonify({"resposta":resposta.content})

#Rodar o nosso app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000)