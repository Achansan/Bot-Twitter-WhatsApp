import os
import time
import tweepy
from googletrans import Translator
from twilio.rest import Client

print("🔧 Inicializando o bot...")

# ========== CONFIGURAÇÕES VIA VARIÁVEIS DE AMBIENTE ==========
twitter_api_key = os.getenv('TWITTER_API_KEY')
twitter_api_secret = os.getenv('TWITTER_API_SECRET')
twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
twitter_access_secret = os.getenv('TWITTER_ACCESS_SECRET')

twilio_sid = os.getenv('TWILIO_SID')
twilio_token = os.getenv('TWILIO_TOKEN')
twilio_from = os.getenv('TWILIO_FROM')  # Ex: whatsapp:+14155238886
twilio_to = os.getenv('TWILIO_TO')      # Ex: whatsapp:+55SEUNUMERO

usuario_twitter = os.getenv('TWITTER_USER')  # Ex: "PlayStation"

# ========== VERIFICANDO VARIÁVEIS ==========
print("🔍 Verificando variáveis de ambiente...")
if not all([twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_secret,
            twilio_sid, twilio_token, twilio_from, twilio_to, usuario_twitter]):
    print("❌ Erro: uma ou mais variáveis de ambiente não estão definidas!")
    exit(1)

# ========== INICIAR APIs ==========
try:
    print("🔌 Conectando à API do Twitter...")
    auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
    auth.set_access_token(twitter_access_token, twitter_access_secret)
    api = tweepy.API(auth)
    print("✅ Twitter conectado com sucesso.")
except Exception as e:
    print(f"❌ Erro ao conectar ao Twitter: {e}")
    exit(1)

try:
    print("🔌 Conectando à API do Twilio...")
    twilio_client = Client(twilio_sid, twilio_token)
    print("✅ Twilio conectado com sucesso.")
except Exception as e:
    print(f"❌ Erro ao conectar ao Twilio: {e}")
    exit(1)

translator = Translator()

# ========== LÓGICA DO BOT ==========
print("🤖 Bot iniciado e monitorando...")

ultimo_tweet_id = None

while True:
    try:
        print(f"🔄 Verificando novos tweets de @{usuario_twitter}...")
        tweets = api.user_timeline(screen_name=usuario_twitter, count=1, tweet_mode="extended")

        if tweets:
            tweet = tweets[0]
            tweet_id = tweet.id
            texto_original = tweet.full_text

            print(f"📌 Último tweet capturado: {tweet_id}")

            if tweet_id != ultimo_tweet_id:
                print("✨ Novo tweet detectado!")
                ultimo_tweet_id = tweet_id

                traducao = translator.translate(texto_original, src='auto', dest='pt').text
                print("🌐 Tradução concluída.")

                mensagem = f"🕊 Novo Tweet de @{usuario_twitter}:\n\n📜 Original:\n{texto_original}\n\n🌎 Traduzido:\n{traducao}"

                twilio_client.messages.create(
                    from_=twilio_from,
                    to=twilio_to,
                    body=mensagem
                )
                print("✅ Mensagem enviada no WhatsApp com sucesso!")
            else:
                print("⏳ Nenhum tweet novo.")

        else:
            print("🚫 Nenhum tweet encontrado.")

    except Exception as e:
        print(f"❌ Erro durante execução: {e}")

    print("🕐 Aguardando 5 minutos para próxima checagem...\n")
    time.sleep(300)  # 300 segundos = 5 minutos
