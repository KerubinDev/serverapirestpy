from flask import jsonify, request
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

    
    def get_leads(self):
        # Obtém os parâmetros 'page', 'per_page' e 'name' da URL, com valores padrão caso não sejam fornecidos
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search_name = request.args.get('name', '', type=str)

        # Chama o serviço para obter leads, passando o nome e parâmetros de paginação
        leads_pagination = self.lead_service.get_leads_by_name_paginated(search_name, page, per_page)

        # Serializa os leads para o formato JSON
        leads = [lead.as_dict() for lead in leads_pagination.items]

        # Retorna a resposta com os dados da paginação
        return jsonify({
            'leads': leads,
            'page': leads_pagination.page,
            'per_page': leads_pagination.per_page,
            'total_pages': leads_pagination.pages,
            'total_leads': leads_pagination.total
        })

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