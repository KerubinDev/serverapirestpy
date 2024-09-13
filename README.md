# API de Leads - Documentação

## Sumário

1. [Introdução](#introdução)
2. [Configuração do Projeto](#configuração-do-projeto)
3. [Instalação e Dependências](#instalação-e-dependências)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Endpoints da API](#endpoints-da-api)
    - [Autenticação JWT](#autenticação-jwt)
    - [GET /leads](#get-leads)
    - [POST /leads](#post-leads)
    - [PUT /leads/{id}](#put-leadsid)
    - [DELETE /leads/{id}](#delete-leadsid)
6. [Testes](#testes)
7. [Como Contribuir](#como-contribuir)

---

## Introdução

Esta API foi desenvolvida para gerenciar Leads, permitindo a criação, listagem, atualização e remoção de registros. Ela utiliza o framework Flask e segue as melhores práticas de autenticação via JWT. Este guia foi elaborado para fornecer todas as instruções necessárias para o uso e entendimento da API.

---

## Configuração do Projeto

Antes de começar, você deve garantir que tem as ferramentas necessárias instaladas em seu ambiente de desenvolvimento:

- **Python 3.12+**
- **Flask**
- **Flask-JWT-Extended**
- **Flask-SQLAlchemy**

---

## Instalação e Dependências

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/serverapirestpy.git
   cd serverapirestpy
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados:

   ```bash
   python setup_database.py
   ```

---

## Estrutura do Projeto

```
serverapirestpy/
│
├── app.py               # Arquivo principal da aplicação Flask
├── api_handler.py       # Lógica para manipulação de endpoints
├── models.py            # Definições dos modelos de banco de dados
├── database.py          # Configuração e conexão com o banco de dados
├── test_api.py          # Testes unitários para a API
├── setup_database.py    # Script para configuração do banco de dados
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação do projeto
```

---

## Endpoints da API

### Autenticação JWT

Todos os endpoints que manipulam dados de leads são protegidos por autenticação JWT. Para acessar esses endpoints, você deve primeiro obter um token JWT válido.

- **POST** `/auth/login`: Retorna um token JWT após o login.
  
  **Exemplo de retorno**:
  
  ```json
  {
    "access_token": "seu_token_jwt_aqui"
  }
  ```

### GET /leads

Este endpoint lista todos os leads cadastrados no sistema.

- **Método**: `GET`
- **URL**: `/leads`
- **Autenticação**: Requer token JWT
- **Resposta**:
  - **200 OK**: Retorna uma lista de leads.

**Exemplo de resposta**:

```json
{
  "leads": [
    {
      "id": 1,
      "nome": "John Doe",
      "email": "john.doe@example.com",
      "telefone": "(11) 1234-5678"
    }
  ]
}
```

### POST /leads

Este endpoint cria um novo lead no sistema.

- **Método**: `POST`
- **URL**: `/leads`
- **Autenticação**: Requer token JWT
- **Corpo da Requisição**:
  - `nome`: Nome do lead (string)
  - `email`: E-mail do lead (string)
  - `telefone`: Telefone do lead (string)

**Exemplo de corpo da requisição**:

```json
{
  "nome": "Jane Doe",
  "email": "jane.doe@example.com",
  "telefone": "(11) 9876-5432"
}
```

**Exemplo de resposta**:

```json
{
  "message": "Lead criado com sucesso!",
  "lead": {
    "id": 2,
    "nome": "Jane Doe",
    "email": "jane.doe@example.com",
    "telefone": "(11) 9876-5432"
  }
}
```

### PUT /leads/{id}

Este endpoint atualiza os dados de um lead existente.

- **Método**: `PUT`
- **URL**: `/leads/{id}`
- **Autenticação**: Requer token JWT
- **Corpo da Requisição**: (mesmo formato do `POST`)

**Exemplo de corpo da requisição**:

```json
{
  "nome": "John Smith",
  "email": "john.smith@example.com",
  "telefone": "(11) 9999-8888"
}
```

**Exemplo de resposta**:

```json
{
  "message": "Lead atualizado com sucesso!",
  "lead": {
    "id": 1,
    "nome": "John Smith",
    "email": "john.smith@example.com",
    "telefone": "(11) 9999-8888"
  }
}
```

### DELETE /leads/{id}

Este endpoint deleta um lead do sistema.

- **Método**: `DELETE`
- **URL**: `/leads/{id}`
- **Autenticação**: Requer token JWT

**Exemplo de resposta**:

```json
{
  "message": "Lead deletado com sucesso!"
}
```

---

## Testes

Para garantir a funcionalidade da API, foram implementados testes automatizados usando o **pytest**. Para rodar os testes, basta executar:

```bash
pytest
```

### Cobertura dos Testes

- **test_get_leads**: Verifica se a listagem de leads está correta.
- **test_create_lead**: Verifica se a criação de um lead funciona corretamente.
- **test_update_lead**: Verifica se a atualização de um lead ocorre sem erros.
- **test_delete_lead**: Verifica se a deleção de um lead é feita corretamente.
- **test_protected_routes_without_token**: Testa o acesso a rotas protegidas sem autenticação.

---

## Como Contribuir

Se você quiser contribuir com este projeto, siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma nova branch para suas mudanças:

   ```bash
   git checkout -b minha-feature
   ```

3. Faça as mudanças necessárias e adicione os commits:

   ```bash
   git commit -m "Minha nova feature"
   ```

4. Envie suas mudanças para o repositório remoto:

   ```bash
   git push origin minha-feature
   ```

5. Abra um Pull Request explicando suas alterações.

---

## Licença

Este projeto é licenciado sob a licença Apache 2.0 - consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.
