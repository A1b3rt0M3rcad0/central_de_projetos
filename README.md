# 🏛 Central de Projetos – Gabinete de Projetos

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.40-red.svg)](https://www.sqlalchemy.org/)
[![Tests](https://img.shields.io/badge/tests-226%20passed-brightgreen.svg)](https://github.com/your-repo/central-de-projetos)
[![Status](https://img.shields.io/badge/status-Produção-brightgreen.svg)](https://github.com/your-repo/central-de-projetos)

## 📌 Visão Geral

Sistema interno para gestão de projetos legislativos municipais desenvolvido com arquitetura limpa e boas práticas de desenvolvimento. Permite o acompanhamento completo de projetos legislativos, incluindo:

### 🎯 Funcionalidades Principais

- **Gestão de Projetos**: Controle completo do ciclo de vida dos projetos legislativos
- **Acompanhamento de Andamento**: Monitoramento em tempo real do status e progresso
- **Gestão Financeira**: Controle de verba disponível e gastos
- **Cronograma**: Datas de início, estimada de conclusão e finalização
- **Classificação**: Tipos de projetos e status organizacionais
- **Responsabilidades**: Vereadores, fiscais e empresas envolvidas
- **Documentação**: Acesso centralizado aos documentos de cada projeto
- **Autenticação**: Sistema seguro de login para vereadores e assessores

### 🏗️ Arquitetura

- **Clean Architecture**: Separação clara entre domínio, casos de uso e infraestrutura
- **Domain-Driven Design**: Modelos de domínio bem definidos
- **Repository Pattern**: Abstração de acesso a dados
- **Dependency Injection**: Composição flexível de dependências

---

## 🚀 Stack Tecnológica

### Backend

- **Linguagem**: Python 3.12+
- **Framework**: FastAPI (API REST moderna e rápida)
- **ORM**: SQLAlchemy 2.0 (mapeamento objeto-relacional)
- **Banco de Dados**: MySQL (principal) + MongoDB (documentos) + Redis (cache)
- **Autenticação**: JWT + bcrypt para senhas
- **Validação**: Pydantic (validação de dados)

### Ferramentas de Desenvolvimento

- **Gerenciador de Pacotes**: UV (Astral) - rápido e moderno
- **Testes**: pytest (framework de testes)
- **Linting**: pylint (análise estática de código)
- **Pre-commit**: Hooks para qualidade de código
- **Migrações**: Alembic (controle de versão do banco)

### Infraestrutura

- **Documentação**: OpenAPI/Swagger (gerada automaticamente)
- **Rate Limiting**: Proteção contra abuso da API
- **CORS**: Configuração para frontend
- **Logs**: Sistema estruturado de logging

---

## 📦 Estrutura do Projeto

```
central_de_projetos/
├── src/
│   ├── auth/                    # Autenticação e autorização
│   │   ├── config/             # Configurações de auth
│   │   └── encrypt/            # Criptografia
│   ├── data/                   # Camada de dados
│   │   ├── interface/          # Interfaces dos repositórios
│   │   └── use_cases/          # Implementação dos casos de uso
│   ├── domain/                 # Regras de negócio puras
│   │   ├── entities/           # Entidades do domínio
│   │   ├── use_cases/          # Interfaces dos casos de uso
│   │   └── value_objects/      # Objetos de valor
│   ├── errors/                 # Sistema de erros personalizados
│   │   ├── http/              # Erros HTTP
│   │   ├── repository/        # Erros de repositório
│   │   └── use_cases/         # Erros de casos de uso
│   ├── infra/                 # Infraestrutura
│   │   ├── mongo/             # MongoDB
│   │   ├── raven/             # RavenDB
│   │   ├── redis/             # Redis
│   │   └── relational/        # MySQL + SQLAlchemy
│   ├── logs/                  # Sistema de logs
│   ├── main/                  # Aplicação FastAPI
│   │   ├── composers/         # Composição de dependências
│   │   ├── config/           # Configurações
│   │   └── routes/           # Rotas da API
│   ├── presentation/          # Controllers e interfaces
│   │   ├── controllers/      # Controllers HTTP
│   │   ├── static/          # Arquivos estáticos
│   │   └── templates/       # Templates HTML
│   ├── security/             # Segurança e criptografia
│   └── utils/                # Utilitários
├── migrations/               # Migrações do banco (Alembic)
├── docs/                    # Documentação OpenAPI
├── tests/                   # Testes de integração
└── requirements.txt         # Dependências (gerado pelo UV)
```

---

## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.12+
- MySQL 8.0+
- MongoDB (opcional)
- Redis (opcional)

### 1. Instalando o UV

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clonando e Configurando o Projeto

```bash
# Clone o repositório (acesso restrito)
git clone https://github.com/seu-usuario/central-de-projetos.git
cd central-de-projetos

# Inicialize o ambiente virtual
uv sync

# Ative o ambiente virtual
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 3. Configuração do Banco de Dados

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do Banco de Dados
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/central_de_projetos
TEST_DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/test_central_de_projetos

# Configurações de Autenticação
JWT_SECRET_KEY=sua_chave_secreta_muito_segura
JWT_ALGORITHM=HS256
JWT_EXPIRATION_TIME=3600

# Configurações do Ambiente
HOMOLOGACAO=True  # Para desenvolvimento
DEBUG=True

# Configurações do MongoDB (opcional)
MONGO_URL=mongodb://localhost:27017/central_de_projetos

# Configurações do Redis (opcional)
REDIS_URL=redis://localhost:6379/0
```

### 4. Executando Migrações

```bash
# Crie as tabelas no banco de dados
alembic upgrade head

# Para desenvolvimento, você pode resetar o banco
alembic downgrade base && alembic upgrade head
```

---

## ▶️ Executando a Aplicação

### Desenvolvimento

```bash
# Com ambiente virtual ativo
python main.py

# Ou usando uvicorn diretamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Produção

```bash
# Usando uvicorn com workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Ou usando gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Acessando a Aplicação

- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🧪 Testes

### Executando Testes

```bash
# Todos os testes
pytest

# Com mais detalhes
pytest -v

# Testes específicos
pytest src/infra/relational/repository/_test/

# Com cobertura (requer pytest-cov)
pytest --cov=src --cov-report=html
```

### Estrutura de Testes

- **Testes Unitários**: Testes isolados de componentes
- **Testes de Integração**: Testes com banco de dados real
- **Testes de API**: Testes end-to-end das rotas

### Configuração de Testes

Os testes usam um banco de dados separado (`test_central_de_projetos`) e são executados em transações que são revertidas após cada teste.

---

## 📚 Documentação da API

### Endpoints Principais

#### Autenticação

- `POST /auth/login/fiscal` - Login de fiscal
- `POST /auth/login/user` - Login de usuário

#### Projetos

- `GET /project` - Listar projetos
- `POST /project` - Criar projeto
- `GET /project/{id}` - Obter projeto específico
- `PUT /project/{id}` - Atualizar projeto
- `DELETE /project/{id}` - Deletar projeto

#### Fiscais

- `GET /fiscal` - Listar fiscais
- `POST /fiscal` - Criar fiscal
- `GET /fiscal/{id}` - Obter fiscal específico

#### Documentos

- `POST /document/upload` - Upload de documento
- `GET /document/{project_id}` - Listar documentos do projeto

### Exemplo de Uso

```python
import httpx

# Login
async with httpx.AsyncClient() as client:
    response = await client.post("http://localhost:8000/auth/login/fiscal", json={
        "email": "fiscal@exemplo.com",
        "password": "senha123"
    })
    token = response.json()["token"]

    # Usar token para acessar recursos protegidos
    headers = {"Authorization": f"Bearer {token}"}
    projects = await client.get("http://localhost:8000/project", headers=headers)
```

---

## 🚢 Deploy

### Docker

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instalar UV
RUN pip install uv

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências
RUN uv sync --no-dev

# Copiar código
COPY . .

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://user:pass@db:3306/central_de_projetos
    depends_on:
      - db
      - redis

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: central_de_projetos
      MYSQL_USER: user
      MYSQL_PASSWORD: pass
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine

volumes:
  mysql_data:
```

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - run: |
          pip install uv
          uv sync
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker image
        run: |
          docker build -t central-de-projetos .
          docker push ${{ secrets.REGISTRY }}/central-de-projetos:latest
```

---

## 🔧 Desenvolvimento

### Comandos Úteis

```bash
# Formatar código
uv run black src/

# Linting
uv run pylint src/

# Pre-commit hooks
pre-commit run --all-files

# Criar nova migração
alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Gerar documentação OpenAPI
python generate_docs.py
```

### Padrões de Código

- **PEP 8**: Estilo de código Python
- **Type Hints**: Tipagem estática
- **Docstrings**: Documentação de funções
- **Clean Architecture**: Separação de responsabilidades

### Estrutura de Commits

```
feat: adiciona funcionalidade de upload de documentos
fix: corrige bug na validação de email
docs: atualiza documentação da API
test: adiciona testes para novo endpoint
refactor: refatora lógica de autenticação
```

---

## 🏢 Informações do Projeto

### Propriedade
Este é um projeto privado desenvolvido para o Gabinete de Projetos. Todo o código e documentação são propriedade exclusiva da organização.

### Acesso
- **Repositório**: Acesso restrito apenas para membros autorizados da equipe
- **Documentação**: Interna e confidencial
- **Deploy**: Ambientes controlados e seguros

### Contato Interno
- **Equipe de Desenvolvimento**: dev@gabinete.local
- **Suporte Técnico**: suporte@gabinete.local
- **Gerente de Projeto**: gerente@gabinete.local

---

## 🙏 Agradecimentos

- FastAPI por fornecer um framework incrível
- SQLAlchemy pela excelente ORM
- Comunidade Python por todas as ferramentas open-source
- Equipe do gabinete por confiar no projeto
