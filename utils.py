import random
from models import Lead, db

def generate_leads():
    print("Gerando leads...")
    
    # Listas de dados fictícios
    names = ['John Doe', 'Jane Smith', 'Chris Johnson', 'Patricia Brown', 'Michael Williams']
    interests = ['Tecnologia', 'Saúde', 'Educação', 'Marketing', 'Design']
    emails = [f'user{i}@gmail.com' for i in range(100)]
    used_emails = set()  # Conjunto para acompanhar os e-mails usados localmente

    # Função para garantir e-mails únicos
    def get_unique_email():
        if len(used_emails) >= len(emails):  # Se todos os e-mails forem usados, interrompa
            return None
        while True:
            email = random.choice(emails)
            if email not in used_emails:  # Verifica se o e-mail já foi usado localmente
                used_emails.add(email)
                return email

    # Função para verificar se o email já existe no banco de dados
    def email_exists(email):
        return db.session.query(Lead).filter_by(email=email).first() is not None

    # Gera 100 leads com dados aleatórios
    for i in range(100):
        email = get_unique_email()
        if email is None:  # Se não houver mais e-mails únicos, interrompe o processo
            print(f"Todos os e-mails disponíveis foram usados. Gerados {i} leads no total.")
            break

        if email_exists(email):  # Verifica se o e-mail já está no banco
            continue  # Se o email já existir no banco, pula para a próxima iteração

        name = random.choice(names)
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        temperature = random.uniform(10, 40)
        interest = random.choice(interests)
        telefone = f'+5511{random.randint(60000000, 69999999)}'  # Telefone fictício

        lead = Lead(
            name=name, latitude=latitude, longitude=longitude, 
            temperature=temperature, interest=interest, email=email, telefone=telefone
        )
        db.session.add(lead)

    db.session.commit()  # Commit após adicionar todos os leads gerados
    print("Leads gerados com sucesso!")