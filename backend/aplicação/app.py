from flask import Flask
from config import config

app = Flask(__name__)
app.config.from_object(config) # Isso carrega as configurações que coloquei no config.py

from aplicação.controladores import rotas