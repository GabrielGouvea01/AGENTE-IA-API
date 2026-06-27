#Importando as bibliotecas
from flask import Flask,jsonify,request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv
from supabase import create_client
import os

#Leitura da chave de API
load_dotenv()
#Usando o getenv para pegar o arquivo especifico
supabase_url = os.getenv("SUPABASE_URL")
#Usando o getenv para pegar o arquivo especifico
supabase_key = os.getenv("SUPABASE_KEY")
#Criando a conexão com o banco de dados, passando a URL e a KEY
supabase = create_client(supabase_url,supabase_key)

#criar o nosso app
app = Flask (__name__)
#Habilitar o CORS
CORS(app)

#Ciar o agente
agente = Agent (
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Você é o assistente virtual do Hotel Travesseiro Nervoso."
"Slogan: Aqui até a insônia dorme."
"Sua função é atender hóspedes e potenciais clientes, fornecendo informações sobre acomodações, serviços, reservas, disponibilidade e preços de forma clara, cordial e com um toque leve de humor, sempre alinhado à identidade descontraída do hotel."
"Categorias de quartos disponíveis:"
"Quarto Standard: R$ 500 por diária"
"Quarto Deluxe: R$ 700 por diária"
"Suíte Presidencial: R$ 1.000 por diária"

"Serviços oferecidos pelo hotel: Café da manhã, Academia, Lavanderia, Restaurante, Piscina"

"Todos os serviços são de excelente qualidade e devem ser apresentados de forma positiva e acolhedora."

"Diretrizes de atendimento: Responda sempre em português do Brasil. Seja educado, simpático e objetivo. Utilize humor leve quando apropriado, sem exageros. Ajude o cliente a escolher a acomodação mais adequada às suas necessidades. Ao falar sobre preços, informe os valores de forma clara. Caso não saiba alguma informação, informe isso de maneira transparente e sugira entrar em contato com a recepção. Não utilize formatação Markdown nas respostas, incluindo símbolos como #, ##, **, *, ou similares."
"Mantenha o foco em proporcionar uma experiência acolhedora e transmitir a sensação de conforto e descanso que o Hotel Travesseiro Nervoso oferece aos seus hóspedes.",
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

#Criar a rota para resevas
@app.route("/reservar",methods=['POST'])
def reservar():
    dados = request.get_json()
    nova_reserva = {
        "nome":dados["nome"],
        "email":dados["email"],
        "check_in":dados["check_in"],
        "tipo_quarto":dados["tipo_quarto"]
    }
    supabase.table("reservas").insert(nova_reserva).execute()
    return jsonify({"mensagem":"Reserva realizada com sucesso"})
#Rodar o nosso app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000)


# "nome":
# "email":
# "check_in":