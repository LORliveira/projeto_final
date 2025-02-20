import os

class config:
    # Configurações dos cookies de sessão
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_secreta'
    SESSION_COOKIE_SECURE = True # Faz com que os cookies apenas sejam transmitidos se for uma conexão HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE ='Lax'
    SQLALCHEMY_DATABASE_URI = 'mysql://usuario:senha@localhost/ecommerce'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DEBUG = True