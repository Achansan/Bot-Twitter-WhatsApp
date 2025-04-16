import os
import requests
import time
from googletrans import Translator
from twilio.rest import Client

# ========== CONFIGURAÇÕES VIA VARIÁVEIS DE AMBIENTE ==========

BEARER_TOKEN = os.getenv('TWITTER_API_KEY')  # Agora é o Bearer Token da API V2
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM')  
TWILIO_TO = os.getenv('TWILIO_TO')     

TWITTER_USER = os.getenv('TWITTER_USER')  

# ========== INICIAR APIs ==========

# Twilio Client
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

# Tradutor
translator = Translator()

# ========== FUNÇÕES ==========

# Função para pegar tweets usando a API v2
def get_recent_tweets(bearer_token, twitter_user):
    url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{twitter_user}&tweet.fields=created_at"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Retorna os tweets em formato JSON
    else:
        print(f"Erro ao buscar tweets: {response.status_code}")
        return None

# Função para enviar mensagens via Twilio
def send_whatsapp_message(twilio_sid, twilio_token, from_number, to_number, message):
    client = Client(twilio_sid, twilio_token)
    message = client.messages.create(
        body=message,
        from_=f"whatsapp:{from_number}",
        to=f"whatsapp:{to_number}"
    )
    print(f"Mensagem enviada para {to_number}: {message.body}")

# Função para traduzir o texto
def translate_text(text, target_lang="pt"):
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    return translation.text

# ========== LÓGICA DO BOT ==========

print("Bot iniciado e monitorando...")

# Variável para evitar duplicação de tweets
ultimo_tweet_id = None

# Loop para monitorar os tweets a cada intervalo de tempo
while True:
    try:
        # Pegando os tweets recentes usando a API v2
        tweets = get_recent_tweets(BEARER_TOKEN, TWITTER_USER)
        
        if tweets and 'data' in tweets:
            for tweet in tweets['data']:
                tweet_id = tweet['id']
                texto_original = tweet['text']

                # Verifica se o tweet é novo (não repetido)
                if tweet_id != ultimo_tweet_id:
                    ultimo_tweet_id = tweet_id

                    # Traduzir o texto do tweet
                    traducao = translate_text(texto_original)

                    # Montar mensagem para enviar
                    mensagem = f"🕊 Novo Tweet de @{TWITTER_USER}:\n\n📜 Original:\n{texto_original}\n\n🌎 Traduzido:\n{traducao}"

                    # Enviar mensagem no WhatsApp via Twilio
                    send_whatsapp_message(TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, TWILIO_TO, mensagem)

                    print("Tweet enviado com sucesso!")
        else:
            print("Nenhum tweet encontrado.")
    
    except Exception as e:
        print(f"Erro: {e}")
    
    # Espera 5 minutos antes de verificar novamente
    time.sleep(300)  # 300 segundos = 5 minutos
