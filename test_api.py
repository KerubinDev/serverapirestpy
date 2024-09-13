import pytest
from app import app
from database import db
from flask_jwt_extended import create_access_token
from models import Lead  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados temporário em memória
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        # Limpar o banco de dados após os testes
        with app.app_context():
            db.session.remove()
            db.drop_all()

def create_test_lead():
    return {
        "name": "Teste Lead",
        "latitude": 120,
        "longitude": 180,
        "temperature": 20,
        "interest": "Gaming",
        "email": "test@example.com",
        "telefone": "+5511999999999"
    }

def create_test_token(client):
    with app.app_context():
        access_token = create_access_token(identity='admin')
    return access_token

def test_get_leads(client):
    """Teste para verificar a listagem de leads."""
    response = client.get('/leads')
    assert response.status_code == 200
    assert response.get_json() == []  # Inicialmente não deve haver leads

def test_create_lead(client):
    """Teste para verificar a criação de um lead."""
    # Primeiro, obtenha um token JWT
    token = create_test_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    # Criação de um lead
    lead_data = create_test_lead()
    response = client.post('/leads', json=lead_data, headers=headers)
    
    assert response.status_code == 201
    assert response.get_json()['message'] == "Lead criado com sucesso!"

def test_update_lead(client):
    """Teste para verificar a atualização de um lead."""
    token = create_test_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    # Criando um lead primeiro
    lead_data = create_test_lead()
    client.post('/leads', json=lead_data, headers=headers)

    # Atualizando o lead
    updated_data = {
        "name": "Updated Lead",
        "latitude": 130,
        "longitude": 150,
        "temperature": 25,
        "interest": "Valorant",
        "email": "updated@example.com",
        "telefone": "+5511988888888"
    }
    response = client.put('/leads/1', json=updated_data, headers=headers)
    
    assert response.status_code == 200
    assert response.get_json()['message'] == "Lead atualizado com sucesso!"

def test_delete_lead(client):
    """Teste para verificar a deleção de um lead."""
    token = create_test_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    # Criando um lead para deletar
    lead_data = create_test_lead()
    client.post('/leads', json=lead_data, headers=headers)

    # Deletando o lead
    response = client.delete('/leads/1', headers=headers)
    
    assert response.status_code == 200
    assert response.get_json()['message'] == "Lead deletado com sucesso!"

def test_protected_routes_without_token(client):
    """Teste para verificar o acesso a rotas protegidas sem token."""
    lead_data = create_test_lead()
    
    # Tentando acessar rotas protegidas sem o token
    create_response = client.post('/leads', json=lead_data)
    update_response = client.put('/leads/1', json=lead_data)
    delete_response = client.delete('/leads/1')
    
    assert create_response.status_code == 401
    assert update_response.status_code == 401
    assert delete_response.status_code == 401