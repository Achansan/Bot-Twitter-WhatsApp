import os
import time
import tweepy
from googletrans import Translator
from twilio.rest import Client

# ========== CONFIGURAÇÕES VIA VARIÁVEIS DE AMBIENTE ==========
twitter_api_key = os.getenv('TWITTER_API_KEY')
twitter_api_secret = os.getenv('TWITTER_API_SECRET')
twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
twitter_access_secret = os.getenv('TWITTER_ACCESS_SECRET')

twilio_sid = os.getenv('TWILIO_SID')
twilio_token = os.getenv('TWILIO_TOKEN')
twilio_from = os.getenv('TWILIO_FROM')  # Ex: whatsapp:+14155238886 (Twilio Sandbox)
twilio_to = os.getenv('TWILIO_TO')      # Ex: whatsapp:+55SEUNUMERO

usuario_twitter = os.getenv('TWITTER_USER')  # Ex: "PlayStation" (sem @)

# ========== INICIAR APIs ==========
# Twitter
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)

# Twilio
client = Client(twilio_sid, twilio_token)

# Tradutor
translator = Translator()

# ========== LÓGICA DO BOT ==========
print("Bot iniciado e monitorando...")

ultimo_tweet_id = None

while True:
    try:
        tweets = api.user_timeline(screen_name=usuario_twitter, count=1, tweet_mode="extended")

        if tweets:
            tweet = tweets[0]
            tweet_id = tweet.id
            texto_original = tweet.full_text

            if tweet_id != ultimo_tweet_id:
                ultimo_tweet_id = tweet_id

                # Traduzir
                traducao = translator.translate(texto_original, src='auto', dest='pt').text

                # Montar mensagem
                mensagem = f"🕊 Novo Tweet de @{usuario_twitter}:\n\n📜 Original:\n{texto_original}\n\n🌎 Traduzido:\n{traducao}"

                # Enviar no WhatsApp
                client.messages.create(
                    from_=twilio_from,
                    to=twilio_to,
                    body=mensagem
                )

                print("Tweet enviado com sucesso!")
        else:
            print("Nenhum tweet encontrado.")

    except Exception as e:
        print(f"Erro: {e}")

    time.sleep(60)  # Espera 60 segundos antes de checar novamente
