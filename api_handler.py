from flask import Flask, jsonify, request
from lead_service import LeadService

class LeadAPIHandler:
    def __init__(self, app, db):
        self.app = app
        self.lead_service = LeadService(db)

        # Define as rotas
        self.app.add_url_rule('/leads', view_func=self.get_leads, methods=['GET'])
        self.app.add_url_rule('/leads/<int:id>', view_func=self.get_lead, methods=['GET'])
        self.app.add_url_rule('/leads', view_func=self.create_lead, methods=['POST'])
        self.app.add_url_rule('/leads/<int:id>', view_func=self.update_lead, methods=['PUT'])
        self.app.add_url_rule('/leads/<int:id>', view_func=self.delete_lead, methods=['DELETE'])

    # Retorna todos os leads
    def get_leads(self):
        leads = self.lead_service.get_all_leads()
        return jsonify([lead.as_dict() for lead in leads])

    # Retorna um lead específico
    def get_lead(self, id):
        lead = self.lead_service.get_lead_by_id(id)
        return jsonify(lead.as_dict())

    # Cria um novo lead
    def create_lead(self):
        data = request.json
        email = data['email']

        # Verifica se o e-mail já existe
        if self.lead_service.email_exists(email):
            return jsonify({"error": "Este e-mail já está sendo utilizado por outro lead."}), 400

        self.lead_service.create_lead(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            temperature=data['temperature'],
            interest=data['interest'],
            email=email,  # Novo campo
            telefone=data['telefone']  # Novo campo
        )
        return jsonify({"message": "Lead criado com sucesso!"}), 201

    # Atualiza um lead existente
    def update_lead(self, id):
        data = request.json
        email = data['email']

        # Verifica se o e-mail já existe e se não pertence ao lead sendo atualizado
        lead = self.lead_service.get_lead_by_id(id)
        if lead.email != email and self.lead_service.email_exists(email):
            return jsonify({"error": "Este e-mail já está sendo utilizado por outro lead."}), 400

        self.lead_service.update_lead(
            lead_id=id,
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            temperature=data['temperature'],
            interest=data['interest'],
            email=email,  # Novo campo
            telefone=data['telefone']  # Novo campo
        )
        return jsonify({"message": "Lead atualizado com sucesso!"})

    # Deleta um lead
    def delete_lead(self, id):
        self.lead_service.delete_lead(id)
        return jsonify({"message": "Lead deletado com sucesso!"})
