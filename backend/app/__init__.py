from flask import Flask
from backend.app.config import config
from backend.app.controladores.DataRecord import DataRecord

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config.from_object(config) # Isso carrega as configurações que coloquei no config.py

ctl = DataRecord()

from backend.app.controladores import rotas