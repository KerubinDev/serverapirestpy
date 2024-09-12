import random
from models import Lead, db

def generate_leads():
    print("Gerando leads...")
    names = ['John Doe', 'Jane Smith', 'Chris Johnson', 'Patricia Brown', 'Michael Williams']
    interests = ['Tecnologia', 'Saúde', 'Educação', 'Marketing', 'Design']
    emails = [f'user{i}@example.com' for i in range(100)]

    used_emails = set()

    def get_unique_email():
        while True:
            email = random.choice(emails)
            if email not in used_emails:
                used_emails.add(email)
                return email  # Mover o return aqui para garantir que o email seja retornado somente se for único

    for _ in range(100):
        name = random.choice(names)
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        temperature = random.uniform(10, 40)
        interest = random.choice(interests)
        email = get_unique_email()  # Usar a função para garantir um email único
        telefone = f'+5511{random.randint(60000000, 69999999)}'  # Gerar telefone fictício

        lead = Lead(name=name, latitude=latitude, longitude=longitude, temperature=temperature, interest=interest, email=email, telefone=telefone)
        db.session.add(lead)

    db.session.commit()  # Commit após adicionar todos os leads
    print("Leads gerados com sucesso!")
