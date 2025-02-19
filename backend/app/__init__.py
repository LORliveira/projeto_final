from flask import Flask
from backend.app.config import config

app = Flask(__name__)
app.config.from_object(config) # Isso carrega as configurações que coloquei no config.py

from backend.app.controladores import rotas