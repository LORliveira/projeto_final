
from flask import Flask, Fla

app = Flask(__name__)

@app.route('/')
def serve_frontend():
    return Fla('../frontend/build', 'index.html')

@app.route('/api')
def api_endpoint():
    return {"message": "Teste"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
