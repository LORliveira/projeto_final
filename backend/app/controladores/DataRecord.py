import json
import uuid
import os
from flask import session
from collections import defaultdict
from backend.app.modelos.user_account import UserAccount
from backend.app.controladores.classes import Produto, Categoria

class DataRecord:
    def __init__(self):
        self.__user_accounts = []  
        self.__authenticated_users = {}  
        self.produtos = []
        self.categorias = {}
        self.carrinhos = defaultdict(list)
        self.pedidos = []
        self.read()

    def read(self):
        # Carrega usuários
        try:
            user_file = os.path.join(os.path.dirname(__file__), "..", "db", "user_accounts.json")
            with open(user_file, "r") as f:
                users = json.load(f)
                self.__user_accounts = [UserAccount(**u) for u in users]
        except FileNotFoundError:
            self.__user_accounts = [UserAccount('Guest', '000000', 'guest@example.com')]

        # Carrega produtos
        try:
            products_file = os.path.join(os.path.dirname(__file__), "..", "db", "products.json")
            with open(products_file, "r") as f:
                products = json.load(f)
                self.produtos = [Produto(**p) for p in products]
        except FileNotFoundError:
            self.produtos = []

        # Carrega categorias
        try:
            categories_file = os.path.join(os.path.dirname(__file__), "..", "db", "categories.json")
            with open(categories_file, "r") as f:
                categories_data = json.load(f)
                self.categorias = {
                    cat["nome"]: Categoria(cat["nome"]) for cat in categories_data
                }
                # Associa produtos às categorias
                for cat in categories_data:
                    for prod in cat["produtos"]:
                        produto = next(p for p in self.produtos if p.nome == prod["nome"])
                        self.categorias[cat["nome"]].add_produto(produto)
        except FileNotFoundError:
            self.populate_initial_data()

    def save(self, data_type="all"):
        # Salva usuários
        if data_type in ["all", "users"]:
            user_file = os.path.join(os.path.dirname(__file__), "..", "db", "user_accounts.json")
            with open(user_file, "w") as f:
                json.dump([vars(u) for u in self.__user_accounts], f, indent=4)

        # Salva produtos
        if data_type in ["all", "produtos"]:
            produtos_file = os.path.join(os.path.dirname(__file__), "..", "db", "products.json")
            with open(produtos_file, "w") as f:
                json.dump([vars(p) for p in self.produtos], f, indent=4)

        # Salva categorias
        if data_type in ["all", "categorias"]:
            categorias_file = os.path.join(os.path.dirname(__file__), "..", "db", "categorias.json")
            with open(categorias_file, "w") as f:
                categories_data = []
                for cat in self.categorias.values():
                    category_entry = {
                        "nome": cat.nome,
                        "produtos": [vars(p) for p in cat.produtos]
                    }
                    categories_data.append(category_entry)
                json.dump(categories_data, f, indent=4)

    def populate_initial_data(self):
        # Popula dados iniciais se não houver arquivos
        initial_products = [
            Produto("Sofá Retrátil", 2500.0, 10, "Sala"),
            Produto("Mesa de Centro", 800.0, 15, "Sala"),
            Produto("Cama Queen Size", 3500.0, 12, "Quarto")
        ]

        self.produtos.extend(initial_products)
        self.categorias = {
            "Sala": Categoria("Sala"),
            "Quarto": Categoria("Quarto")
        }

        for p in initial_products:
            if p.categoria in self.categorias:
                self.categorias[p.categoria].add_produto(p)

        self.save()


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