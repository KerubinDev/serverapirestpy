from models import Lead

class LeadService:
    def __init__(self, db):
        self.db = db

    def email_exists(self, email):
            # Verifica se o e-mail já existe no banco de dados
            existing_lead = Lead.query.filter_by(email=email).first()
            return existing_lead is not None
    
    def create_lead(self, name, latitude, longitude, temperature, interest, email, telefone):
        lead = Lead(
            name=name,
            latitude=latitude,
            longitude=longitude,
            temperature=temperature,
            interest=interest,
            email=email,  # Novo campo
            telefone=telefone  # Novo campo
        )
        self.db.session.add(lead)
        self.db.session.commit()

    def get_all_leads(self):
        return Lead.query.all()

    def get_lead_by_id(self, lead_id):
        return Lead.query.get_or_404(lead_id)

    def update_lead(self, lead_id, name, latitude, longitude, temperature, interest, email, telefone):
        lead = self.get_lead_by_id(lead_id)
        lead.name = name
        lead.latitude = latitude
        lead.longitude = longitude
        lead.temperature = temperature
        lead.interest = interest
        lead.email = email  # Atualizando o novo campo
        lead.telefone = telefone  # Atualizando o novo campo
        self.db.session.commit()

    def delete_lead(self, lead_id):
        lead = self.get_lead_by_id(lead_id)
        self.db.session.delete(lead)
        self.db.session.commit()
    
    def get_all_leads_paginated(self, page, per_page):
        return Lead.query.paginate(page=page, per_page=per_page, error_out=False)
    
    def get_leads_by_name_paginated(self, search_name, page, per_page):
        query = Lead.query

        if search_name:
            query = query.filter(Lead.name.ilike(f"%{search_name}%"))

        return query.paginate(page=page, per_page=per_page, error_out=False)
