import random
from models import Lead, db

# Função para gerar leads fictícios
def generate_leads():
    names = ['John Doe', 'Jane Smith', 'Chris Johnson', 'Patricia Brown', 'Michael Williams']
    interests = ['Tecnologia', 'Saúde', 'Educação', 'Marketing', 'Design']

    for _ in range(100):
        name = random.choice(names)
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        temperature = random.uniform(10, 40)
        interest = random.choice(interests)

        lead = Lead(name, latitude, longitude, temperature, interest)
        db.session.add(lead)

    db.session.commit()
 