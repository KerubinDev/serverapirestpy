from flask import Flask, jsonify, request
from database import DatabaseConnection
from api_handler import LeadAPIHandler
from utils import generate_leads
from flask_jwt_extended import create_access_token, JWTManager
from datetime import timedelta

# Configuração básica do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'minha-chave-secreta'

# Inicializando a conexão com o banco de dados
db_connection = DatabaseConnection(app)
db_connection.initialize_db(app)
jwt = JWTManager(app)

# Gerando leads fictícios
with app.app_context():
    generate_leads() 

# Inicializando a API com as rotas
api_handler = LeadAPIHandler(app, db_connection.get_db())

users = {
    "admin": "password123",
    "user": "pass456"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Verificação simples de usuário e senha (pode ser substituído por um banco de dados)
    if username in users and users[username] == password:
        # Gera o token JWT com validade de 1 dia
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
        return jsonify(access_token=access_token)
    else:
        return jsonify({"message": "Credenciais inválidas!"}), 401

if __name__ == '__main__':
    app.run(debug=True)