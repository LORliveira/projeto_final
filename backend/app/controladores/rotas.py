from flask import render_template, redirect, request, session, url_for, flash
from backend.app import app
from backend.app.controladores.DataRecord import DataRecord
from backend.app.controladores.classes import (Produto, Carrinho, Pedido, Categoria, produtos, categorias, carrinhos, pedidos, popular_categorias)

ctl = DataRecord() # Não esquecer de fazer o data record que o controlador de dados


@app.route('/')
def index():
    return render_template('index.html', produtos=produtos, categorias=categorias)

@app.route('/pagina', methods=['GET'])
@app.route('/pagina/<username>', methods=['GET'])
def action_pagina(username=None):
    if not username:
        return render_template('pagina.html', transfered=False)
    else:
        info = ctl.work_with_parameter(username)
        if not info:
             return redirect(url_for('index'))
        else:
            return render_template('pagina.html', transfered=True, data=info)

@app.route('/portal', methods=['GET', 'POST'])
def portal():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        session_id, username = ctl.authenticate_user(username, password)
        if session_id:
            session['session_id'] = session_id
            return render_template(url_for('portal'))
        else:
            return redirect(url_for('portal'))
    return render_template('portal.html')

@app.route('/logout', methods=['POST'])
def logout():
    ctl.logout_user()
    session.pop('session_id', None)
    return redirect(url_for('index'))

@app.route('/registrar', methods=['GET'])
def registrar():
    return render_template('registrar.html')  

@app.route('/processar_registro', methods=['POST'])
def processar_registro():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    # Tenta registrar o usuário
    if ctl.registrar_usuario(username, password, email):
        flash('Registro bem-sucedido! Faça login para continuar.', 'success')
        return redirect(url_for('portal'))  
    else:
        flash('Nome de usuário já existe. Escolha outro nome.', 'error')
        return redirect(url_for('registrar')) 
            
@app.route("/add_carrinho/<nome>")
def add_carrinho(nome):
    produto = next(p for p in produtos if p.nome == nome)
    carrinho = Carrinho(session.get("usuario", "guest"))
    carrinho.addProd(produto)
    carrinhos[session.get("usuario", "guest")] = carrinho
    return redirect("/")

@app.route("/rem_carrinho/<nome>")
def rem_carrinho(nome):
    carrinho = carrinhos.get(session.get("usuario", "guest"))
    if carrinho:
        carrinho.remProd(nome)
    return redirect("/carrinho")

@app.route("/carrinho")
def ver_carrinho():
    carrinho = carrinhos.get(session.get("usuario", "guest"), Carrinho("guest"))
    return render_template("carrinho.html", carrinho=carrinho)

@app.route("/finalizar")
def finalizar():
    carrinho = carrinhos.get(session.get("usuario", "guest"))
    if carrinho:
        carrinho.finalizarCompra()
    return redirect("/pedidos")
    
@app.route("/pedidos")
def ver_pedidos():
    return render_template("pedidos.html", pedidos=pedidos)

@app.route("/sala")
def sala():
    return render_template("sala.html", produtos=categorias["sala"].produtos)

@app.route("/quarto")
def quarto():
    return render_template("quarto.html", produtos=categorias["quarto"].produtos)

@app.route("/banheiro")
def banheiro():
    return render_template("banheiro.html", produtos=categorias["banheiro"].produtos)

@app.route("/cozinha")
def cozinha():
    return render_template("cozinha.html", produtos=categorias["cozinha"].produtos)
        
@app.route('/api')
def api_endpoint():
    return {"message": "Teste"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)