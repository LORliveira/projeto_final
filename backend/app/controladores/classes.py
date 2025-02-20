from collections import defaultdict

# Simulação de "banco de dados" em memória
produtos = []
categorias = [{"nome": "Eletrônicos"}, {"nome": "Livros"}, {"nome": "Vestuario"}]
carrinhos = defaultdict(list)
pedidos = []

class Produto:
    def __init__(self, nome, preco, quantidade, categoria):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.categoria = categoria

class Carrinho:
    def __init__(self, usuario):
        self.usuario = usuario
        self.listProd = []

    def addProd(self, produto):
        self.listProd.append(produto)

    def remProd(self, produto_nome):
        self.listProd = [p for p in self.listProd if p.nome != produto_nome]

    def finalizarCompra(self):
        total = sum(p.preco for p in self.listProd)
        novo_pedido = Pedido(self.usuario, self.listProd.copy(), total)
        pedidos.append(novo_pedido)
        self.listProd.clear()

class Pedido:
    def __init__(self, usuario, listProd, total):
        self.usuario = usuario
        self.listProd = listProd
        self.total = total
        self.status = "Processando"

    def attStatus(self, novo_status):
        self.status = novo_status

class Categoria:
    def __init__(self, nome):
        self.nome = nome
        self.produtos = []

    def add_produto(self, produto):
        self.produtos.append(produto)

categorias = {
    "sala": Categoria("Sala"),
    "quarto": Categoria("Quarto"),
    "banheiro": Categoria("Banheiro"),
    "cozinha": Categoria("Cozinha")
}

def popular_categorias():
    produtos_sala = [
        Produto("Sofá Retrátil", 2500.0, 10, "Sala"),
        Produto("Mesa de Centro", 800.0, 15, "Sala"),
        Produto("Estante Moderna", 1200.0, 8, "Sala")
    ]
    
    produtos_quarto = [
        Produto("Cama Queen Size", 3500.0, 12, "Quarto"),
        Produto("Guarda-Roupas", 2800.0, 7, "Quarto"),
        Produto("Criado Mudo", 450.0, 20, "Quarto")
    ]
    
    produtos_banheiro = [
        Produto("Espelho Decorativo", 300.0, 25, "Banheiro"),
        Produto("Conjunto Toalhas", 150.0, 30, "Banheiro"),
        Produto("Cabideiro Inox", 200.0, 18, "Banheiro")
    ]
    
    produtos_cozinha = [
        Produto("Fogão 5 Bocas", 1800.0, 10, "Cozinha"),
        Produto("Geladeira Frost-Free", 4500.0, 8, "Cozinha"),
        Produto("Liquidificador Potente", 350.0, 15, "Cozinha")
    ]

    for p in produtos_sala: categorias["sala"].add_produto(p)
    for p in produtos_quarto: categorias["quarto"].add_produto(p)
    for p in produtos_banheiro: categorias["banheiro"].add_produto(p)
    for p in produtos_cozinha: categorias["cozinha"].add_produto(p)

# Inicialização dos dados
if __name__ == "__main__":
    popular_categorias()

    produtos.append(Produto("iPhone", 5000.0, 10, "Eletrônicos"))
    produtos.append(Produto("Python Essentials", 100.0, 5, "Livros"))
    produtos.append(Produto("Notebook Dell", 3500.0, 8, "Eletrônicos"))
    produtos.append(Produto("Camisa Polo", 120.0, 15, "Vestuário"))
    produtos.append(Produto("Headphone Sony", 400.0, 12, "Eletrônicos"))
    produtos.append(Produto("Livro de Flask", 90.0, 7, "Livros"))

   