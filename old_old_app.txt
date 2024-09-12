from flask import Flask, jsonify, request
from models import db, Lead

# Configuração básica do Flask e banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Endpoint GET: Retorna todos os leads
@app.route('/leads', methods=['GET'])
def get_leads():
	leads = Lead.query.all()
	return jsonify([lead.as_dict() for lead in leads])

# Endpoint GET: Retorna um lead específico por ID
@app.route('/leads/<int:id>', methods=['GET'])
def get_lead(id):
	lead = Lead.query.get_or_404(id)
	return jsonify(lead.as_dict())

# Endpoint POST: Cria um novo lead
@app.route('/leads', methods=['POST'])
def create_lead():
	data = request.json
	new_lead = Lead(
    	name=data['name'],
    	latitude=data['latitude'],
    	longitude=data['longitude'],
    	temperature=data['temperature'],
    	interest=data['interest']
	)
	db.session.add(new_lead)
	db.session.commit()
	return jsonify({"message": "Lead criado com sucesso!"}), 201

# Endpoint PUT: Atualiza um lead existente
@app.route('/leads/<int:id>', methods=['PUT'])
def update_lead(id):
	lead = Lead.query.get_or_404(id)
	data = request.json
	lead.name = data['name']
	lead.latitude = data['latitude']
	lead.longitude = data['longitude']
	lead.temperature = data['temperature']
	lead.interest = data['interest']
	db.session.commit()
	return jsonify({"message": "Lead atualizado com sucesso!"})

# Endpoint DELETE: Deleta um lead
@app.route('/leads/<int:id>', methods=['DELETE'])
def delete_lead(id):
	lead = Lead.query.get_or_404(id)
	db.session.delete(lead)
	db.session.commit()
	return jsonify({"message": "Lead deletado com sucesso!"})

if __name__ == '__main__':
	app.run(debug=True) 