from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Tabela associativa para Carrinho e Produto
carrinho_produto = db.Table('carrinho_produto',
    db.Column('carrinho_id', db.Integer, db.ForeignKey('carrinho.id')),
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'))
)

# Tabela associativa para Pedido e Produto
pedido_produto = db.Table('pedido_produto',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id')),
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'))
)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

class Carrinho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    produtos = db.relationship('Produto', secondary=carrinho_produto, lazy='dynamic')

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Processando')
    data = db.Column(db.DateTime, default=datetime.utcnow)
    produtos = db.relationship('Produto', secondary=pedido_produto, lazy='dynamic')

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    carrinhos = db.relationship('Carrinho', backref='usuario', lazy=True)
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)