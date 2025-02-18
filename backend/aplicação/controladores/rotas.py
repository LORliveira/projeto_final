
from flask import render_template, redirect, request, session, url_for
from app import app
from controladores.DataRecord import DataRecord

ctl = DataRecord() # Não esquecer de fazer o data record que o controlador de dados

@app.route('index')
def serve_frontend():
    return ('../frontend/build', 'index.html')

@app.route('/')
def index():
    return render_template('helper.html')

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
            

@app.route('/api')
def api_endpoint():
    return {"message": "Teste"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
