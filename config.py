import os
basedir = os.path.abspath(os.path.dirname(__file__))
import secrets

# Генерация безопасного случайного ключа

class Config(object):
    SECRET_KEY = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join('app.db')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False