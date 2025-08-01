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
- **Banco de Dados**: MySQL (principal) + RavenDB (documentos) + MongoDB (logs) + Redis (cache)
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

## 📁 Estrutura do Projeto

```
central_de_projetos/
├── .vscode/                    # Configurações do VS Code
├── docs/                       # Documentação da API
├── migrations/                 # Migrações do banco de dados
│   └── versions/              # Versões das migrações
└── src/                       # Código fonte principal
    ├── auth/                  # Autenticação e autorização
    │   ├── config/           # Configurações de auth
    │   │   └── interface/    # Interfaces de configuração
    │   └── encrypt/          # Criptografia
    │       └── interface/    # Interfaces de criptografia
    ├── data/                 # Camada de dados (Clean Architecture)
    │   ├── interface/        # Interfaces dos repositórios
    │   └── use_cases/        # Casos de uso da camada de dados
    │       └── _tests/       # Testes dos casos de uso
    ├── domain/               # Camada de domínio (Clean Architecture)
    │   ├── entities/         # Entidades de negócio
    │   ├── use_cases/        # Interfaces dos casos de uso
    │   └── value_objects/    # Objetos de valor
    ├── errors/               # Tratamento de erros
    │   ├── http/            # Erros HTTP
    │   ├── repository/      # Erros de repositório
    │   │   ├── __base/      # Classes base de erro
    │   │   ├── already_exists_error/
    │   │   ├── error_on_delete/
    │   │   ├── error_on_find/
    │   │   ├── error_on_insert/
    │   │   ├── error_on_update/
    │   │   ├── has_related_children/
    │   │   └── not_exists_error/
    │   ├── use_cases/       # Erros de casos de uso
    │   │   └── __base/      # Classes base de erro
    │   └── value_object/    # Erros de objetos de valor
    │       └── __base/      # Classes base de erro
    ├── infra/               # Camada de infraestrutura (Clean Architecture)
    │   ├── mongo/           # Configuração MongoDB
    │   │   ├── config/      # Configurações de conexão
    │   │   │   ├── connection/
    │   │   │   │   └── interface/
    │   │   │   └── interface/
    │   │   ├── documents/   # Documentos MongoDB
    │   │   │   └── tests/
    │   │   ├── models/      # Modelos MongoDB
    │   │   └── repositories/ # Repositórios MongoDB
    │   ├── raven/           # Configuração RavenDB
    │   │   ├── config/      # Configurações de conexão
    │   │   │   └── connection/
    │   │   │       ├── __test/
    │   │   │       └── interface/
    │   │   ├── documents/   # Documentos RavenDB
    │   │   ├── models/      # Modelos RavenDB
    │   │   └── repositories/ # Repositórios RavenDB
    │   │       └── __test/
    │   ├── redis/           # Configuração Redis
    │   │   ├── config/      # Configurações de conexão
    │   │   │   └── connection/
    │   │   ├── models/      # Modelos Redis
    │   │   └── repositories/ # Repositórios Redis
    │   └── relational/      # Configuração banco relacional (MySQL)
    │       ├── config/      # Configurações de conexão
    │       │   ├── base/    # Classes base
    │       │   ├── connection/
    │       │   └── interface/
    │       ├── models/      # Modelos SQLAlchemy
    │       ├── models_v1/   # Versão 1 dos modelos
    │       └── repository/  # Repositórios SQLAlchemy
    │           └── _test/   # Testes dos repositórios
    ├── logs/                # Sistema de logs
    │   ├── config/          # Configurações de log
    │   └── logger/          # Implementação do logger
    ├── main/                # Camada principal (Clean Architecture)
    │   ├── adapters/        # Adaptadores de entrada/saída
    │   ├── composers/       # Composição de dependências
    │   │   ├── _tests/      # Testes de integração
    │   │   └── internal/    # Composições internas
    │   ├── config/          # Configurações da aplicação
    │   │   └── database/    # Configurações de banco
    │   ├── routes/          # Rotas da aplicação
    │   │   ├── api/         # Rotas da API REST
    │   │   │   ├── __base_response/
    │   │   │   ├── __error/
    │   │   │   ├── auth/    # Rotas de autenticação
    │   │   │   │   ├── request_format/
    │   │   │   │   └── response_format/
    │   │   │   ├── bairro/  # Rotas de bairros
    │   │   │   │   ├── bairro_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── document/ # Rotas de documentos
    │   │   │   │   ├── document_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── empresa/ # Rotas de empresas
    │   │   │   │   ├── empresa_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── fiscal/  # Rotas de fiscais
    │   │   │   │   ├── fiscal_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── history_project/ # Rotas de histórico
    │   │   │   │   ├── history_project_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── project/ # Rotas de projetos
    │   │   │   │   ├── project_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── project_bairro/ # Rotas de associação projeto-bairro
    │   │   │   │   ├── project_bairro_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── project_empresa/ # Rotas de associação projeto-empresa
    │   │   │   │   ├── project_empresa_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── project_fiscal/ # Rotas de associação projeto-fiscal
    │   │   │   │   ├── project_fiscal_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── project_type/ # Rotas de tipos de projeto
    │   │   │   │   ├── project_type_response/
    │   │   │   │   └── request_format/
    │   │   │   ├── status/  # Rotas de status
    │   │   │   │   ├── format_request/
    │   │   │   │   └── status_response/
    │   │   │   ├── types/   # Rotas de tipos
    │   │   │   │   ├── request_format/
    │   │   │   │   └── types_response/
    │   │   │   ├── user/    # Rotas de usuários
    │   │   │   │   ├── request_format/
    │   │   │   │   └── user_response/
    │   │   │   └── user_project/ # Rotas de associação usuário-projeto
    │   │   │       ├── request_format/
    │   │   │       └── user_project_response/
    │   │   ├── middleware/  # Middlewares da aplicação
    │   │   ├── mobile/      # Rotas para aplicação mobile
    │   │   │   └── fiscal/  # Rotas específicas para fiscais mobile
    │   │   │       ├── request_format/
    │   │   │       └── response_format/
    │   │   └── web/         # Rotas para aplicação web
    │   │       ├── __test/
    │   │       └── login/
    │   └── templates/       # Templates da aplicação
    ├── presentation/         # Camada de apresentação (Clean Architecture)
    │   ├── controllers/     # Controladores HTTP
    │   │   └── _tests/      # Testes dos controladores
    │   ├── http_types/      # Tipos HTTP (Request/Response)
    │   ├── interface/       # Interfaces dos controladores
    │   ├── static/          # Arquivos estáticos
    │   │   ├── base/        # Arquivos base
    │   │   │   └── icons/   # Ícones
    │   │   ├── login/       # Arquivos de login
    │   │   └── test/        # Arquivos de teste
    │   └── templates/       # Templates HTML
    │       ├── base/        # Templates base
    │       │   ├── components/
    │       │   └── page/
    │       ├── content/     # Conteúdo das páginas
    │       │   └── __test/
    │       └── login/       # Templates de login
    ├── security/            # Segurança e criptografia
    │   ├── cryptography/    # Implementações criptográficas
    │   │   ├── interface/   # Interfaces de criptografia
    │   │   └── utils/       # Utilitários de criptografia
    │   └── value_objects/   # Objetos de valor de segurança
    │       └── interface/   # Interfaces de segurança
    └── utils/               # Utilitários gerais
        └── decorators/      # Decoradores personalizados
```

### 📋 Descrição das Camadas

#### 🏗️ **Clean Architecture**

O projeto segue a arquitetura limpa com 4 camadas principais:

- **`presentation/`**: Interface com usuários (HTTP, Web, Mobile)
- **`domain/`**: Regras de negócio e entidades
- **`data/`**: Casos de uso e acesso a dados
- **`infra/`**: Infraestrutura (banco de dados, APIs externas)

#### 🗄️ **Bancos de Dados**

- **`infra/relational/`**: MySQL (dados principais)
- **`infra/raven/`**: RavenDB (documentos)
- **`infra/mongo/`**: MongoDB (logs)
- **`infra/redis/`**: Redis (cache)

#### 🔐 **Segurança**

- **`auth/`**: Autenticação JWT
- **`security/`**: Criptografia e hash de senhas
- **`middleware/`**: Autorização e rate limiting

---

## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.12+
- MySQL 8.0+
- MongoDB (opcional)
- Redis (opcional)
- RavenDB

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

Crie um arquivo `.env` na raiz do projeto baseado no arquivo `config.example.env`:

```bash
# Copie o arquivo de exemplo
cp config.example.env .env

# Edite o arquivo .env com suas configurações
nano .env
```

Exemplo de configuração mínima:

```env
# Server Config
HOMOLOGACAO=True|False

# AUTH SECRET KEY
SECRET_KEY=YOUR_SECRET_KEY
EXPIRE_TIME_TOKEN=48 # In hours FLOAT
EXPIRE_TIME_REFRESH_TOKEN=7 #In Days FLOAT

# DATABASE CONNECTION
DATABASE=mysql
DRIVE=pymysql
USERNAME=root
PASSWORD=password
HOST=localhost
PORT=3306
DATABASE_NAME=central_de_projetos

# TEST DATABASE CONNECTION
TDATABASE=mysql
TDRIVE=pymysql
TUSERNAME=root
TPASSWORD=password
THOST=localhost
TPORT=3306
TDATABASE_NAME=test_central_de_projetos

# MONGODB
MONGO_HOST=localhost
MONGO_PORT= 27017
MONGO_USERNAME=username | null
MONGO_PASSWORD=password | null
MONGO_DB_NAME=central_de_projetos

# TESTE MONGODB
TMONGO_HOST=localhost
TMONGO_PORT= 27017
TMONGO_USERNAME=username | null
TMONGO_PASSWORD=password | null
TMONGO_DB_NAME=test_central_de_projetos

# RAVEN DATABASE

RAVEN_URL=http://localhost:8080
RAVEN_DATABASE=database_name
RAVEN_CERTIFICATE_PATH=path|null
RAVEN_CERTIFICATE_PASSWORD=password|null
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

Para informações técnicas detalhadas sobre desenvolvimento, consulte o arquivo [DEVELOPMENT.md](DEVELOPMENT.md).

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

## 👨‍💻 Desenvolvedor

### Autor

**Alberto da Silva Mercado**

### Contato

- **Email**: alberto.zimba2013@gmail.com
- **Telefone**: (48) 99162-3022

### Desenvolvimento

Este projeto foi desenvolvido integralmente por Alberto da Silva Mercado, incluindo:

- Arquitetura e design do sistema
- Implementação de todas as funcionalidades
- Configuração de infraestrutura
- Documentação técnica
- Testes e qualidade de código

---

## 🙏 Agradecimentos

- FastAPI por fornecer um framework incrível
- SQLAlchemy pela excelente ORM
- Comunidade Python por todas as ferramentas open-source
- Equipe do gabinete por confiar no projeto
