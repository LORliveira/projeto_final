import json
import uuid
import os
from flask import session
from backend.app.modelos.user_account import UserAccount

class DataRecord:
    def __init__(self):
        self.__user_accounts = []  
        self.__authenticated_users = {}  
        self.read()

    def read(self):
        # Carrega os dados do arquivo JSON
        try:
            file_path = os.path.join(os.path.dirname(__file__), "..", "db", "user_accounts.json")
            with open(file_path, "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount('Guest', '000000', 'guest@example.com'))

    def save(self):
        # Salva os dados dos usuários
        file_path = os.path.join(os.path.dirname(__file__), "..", "db", "user_accounts.json")
        with open(file_path, "w") as arquivo_json:
            user_data = [vars(user) for user in self.__user_accounts]
            json.dump(user_data, arquivo_json, indent=4) 

    def work_with_parameter(self, parameter):
        # Retorna o usuario se bater com o parametro
        for user in self.__user_accounts:
            if user.username == parameter:
                return user
        return None  

    def authenticate_user(self, username, password):
       # Autentica o usuario e cria a sessão desse usuario
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())
                self.__authenticated_users[session_id] = user
                return session_id, username
        return None

    def logout_user(self):
       # Faz o logout
        session_id = session.get('session_id')
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]

    def registrar_usuario(self, username, password, email):
        # Verifica se o usuário já existe
        if any(user.username == username for user in self.__user_accounts):
            return False 

        # Cria um novo usuário
        novo_usuario = UserAccount(username, password, email)
        self.__user_accounts.append(novo_usuario)
        self.save()  # Salva no arquivo JSON
        return True  