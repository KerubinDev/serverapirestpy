from flask import Flask
from models import db
from utils import generate_leads

# Configuração do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco de dados
db.init_app(app)

# Criando as tabelas e populando o banco de dados com leads fictícios
with app.app_context():
	db.create_all()
	generate_leads()

if __name__ == '__main__':
	app.run(debug=True)