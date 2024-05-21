import os
basedir = os.path.abspath(os.path.dirname(__file__))
import secrets
from base64 import b64encode

# Генерация безопасного случайного ключа

class Config(object):
    SECRET_KEY = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join('app.db')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

#создание секретного ключа по необходимости
# generate_secret_key = b64encode(secrets.token_bytes(20)).decode()
sign_in_key = "Jt97dLlwUIToSl1plYv=/+BJKHICb5HU"

