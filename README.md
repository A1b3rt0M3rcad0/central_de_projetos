# 🏛 Central de Projetos – Gabinete de Projetos

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.40-red.svg)](https://www.sqlalchemy.org/)
[![Tests](https://img.shields.io/badge/tests-226%20passed-brightgreen.svg)](https://github.com/your-repo/central-de-projetos)
[![Status](https://img.shields.io/badge/status-Produção-brightgreen.svg)](https://github.com/your-repo/central-de-projetos)

## 📌 Visão Geral

Sistema interno para gestão de projetos legislativos municipais desenvolvido com **Clean Architecture** e boas práticas de desenvolvimento. Permite o acompanhamento completo de projetos legislativos, incluindo gestão de projetos, acompanhamento de andamento, controle financeiro, cronogramas e documentação centralizada.

### 🎯 Funcionalidades Principais

- **Gestão de Projetos**: Controle completo do ciclo de vida dos projetos legislativos
- **Acompanhamento de Andamento**: Monitoramento em tempo real do status e progresso
- **Gestão Financeira**: Controle de verba disponível e gastos
- **Cronograma**: Datas de início, estimada de conclusão e finalização
- **Classificação**: Tipos de projetos e status organizacionais
- **Responsabilidades**: Vereadores, fiscais e empresas envolvidas
- **Documentação**: Acesso centralizado aos documentos de cada projeto
- **Autenticação**: Sistema seguro de login para vereadores e assessores

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

---

## 🏗️ Arquitetura

### Clean Architecture

O projeto segue os princípios da Clean Architecture com as seguintes camadas:

```
┌─────────────────────────────────────┐
│           Presentation              │  ← Controllers, HTTP
├─────────────────────────────────────┤
│              Domain                 │  ← Entidades, Regras de Negócio
├─────────────────────────────────────┤
│               Data                  │  ← Casos de Uso, Repositórios
├─────────────────────────────────────┤
│            Infrastructure           │  ← Banco de Dados, APIs Externas
└─────────────────────────────────────┘
```

### Estrutura de Diretórios

```
src/
├── auth/                    # Autenticação e autorização
│   ├── config/             # Configurações de auth
│   └── encrypt/            # Criptografia
├── data/                   # Camada de dados
│   ├── interface/          # Interfaces dos repositórios
│   └── use_cases/          # Implementação dos casos de uso
├── domain/                 # Regras de negócio puras
│   ├── entities/           # Entidades do domínio
│   ├── use_cases/          # Interfaces dos casos de uso
│   └── value_objects/      # Objetos de valor
├── errors/                 # Sistema de erros personalizados
├── infra/                  # Infraestrutura
│   ├── mongo/             # MongoDB
│   ├── raven/             # RavenDB
│   ├── redis/             # Redis
│   └── relational/        # MySQL + SQLAlchemy
├── logs/                  # Sistema de logs
├── main/                  # Aplicação FastAPI
├── presentation/          # Controllers e interfaces
├── security/             # Segurança e criptografia
└── utils/                # Utilitários
```

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
# Clone o repositório
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

```bash
# Copie o arquivo de exemplo
cp config.example.env .env

# Edite o arquivo .env com suas configurações
nano .env
```

Exemplo de configuração mínima:

```env
# Server Config
HOMOLOGACAO=True

# AUTH SECRET KEY
SECRET_KEY=YOUR_SECRET_KEY
EXPIRE_TIME_TOKEN=48
EXPIRE_TIME_REFRESH_TOKEN=7

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
MONGO_PORT=27017
MONGO_USERNAME=username
MONGO_PASSWORD=password
MONGO_DB_NAME=central_de_projetos

# RAVEN DATABASE
RAVEN_URL=http://localhost:8080
RAVEN_DATABASE=database_name
RAVEN_CERTIFICATE_PATH=path
RAVEN_CERTIFICATE_PASSWORD=password
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

# Com cobertura
pytest --cov=src --cov-report=html

# Testes paralelos
pytest -n auto
```

### Estrutura de Testes

- **Testes Unitários**: Testes isolados de componentes
- **Testes de Integração**: Testes com banco de dados real
- **Testes de API**: Testes end-to-end das rotas

### Configuração de Testes

Os testes usam um banco de dados separado (`test_central_de_projetos`) e são executados em transações que são revertidas após cada teste.

---

## 🔄 Migrações

### Alembic

O projeto usa Alembic para controle de versão do banco de dados.

### Migration Manager

O projeto inclui um script personalizado (`migration_manager.py`) para gerenciar migrações em múltiplos ambientes (teste e produção) usando variáveis de ambiente.

#### Configuração das Variáveis de Ambiente

O script usa as variáveis do arquivo `.env`:

```bash
# Banco de Produção
HOST=localhost
PORT=3306
USERNAME=root
PASSWORD=sua_senha
DATABASE_NAME=central_de_projetos

# Banco de Teste
THOST=localhost
TPORT=3306
TUSERNAME=root
TPASSWORD=sua_senha_teste
TDATABASE_NAME=test_central_de_projetos
```

#### Comandos do Migration Manager

```bash
# Aplicar migrações em ambos os bancos
python migration_manager.py upgrade head --all

# Apenas banco de teste
python migration_manager.py upgrade head --test

# Apenas banco de produção
python migration_manager.py upgrade head --prod

# Reverter migração em ambos os bancos
python migration_manager.py downgrade -1 --all

# Verificar versão atual
python migration_manager.py current --all

# Ver histórico de migrações
python migration_manager.py history --all

# Criar nova migração automática
python migration_manager.py revision --autogenerate -m "descrição da migração" --all
```

#### Funcionalidades do Migration Manager

- 🎯 **Múltiplos ambientes**: Execute em teste, produção ou ambos
- 🔄 **Todos os comandos Alembic**: Aceita qualquer comando do Alembic
- ✅ **Confirmação de segurança**: Sempre pede confirmação antes de executar
- 📊 **Relatório de sucesso**: Mostra quantas operações foram bem-sucedidas
- 🛡️ **Tratamento de erros**: Captura e exibe erros de forma clara

### Comandos Alembic Diretos

```bash
# Criar nova migração
alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1

# Ver histórico
alembic history

# Ver status atual
alembic current

# Ver detalhes de uma migração
alembic show <revision_id>
```

### Boas Práticas

1. **Sempre** gere migrações para mudanças no modelo
2. **Teste** as migrações em ambiente de desenvolvimento primeiro
3. **Use o Migration Manager** para operações em múltiplos ambientes
4. **Documente** mudanças complexas
5. **Faça backup** antes de aplicar em produção
6. **Verifique** o comando antes de confirmar a execução

### Segurança

- ✅ **Sem senhas no código**: Todas as credenciais vêm do arquivo `.env`
- ✅ **Confirmação**: O script sempre pede confirmação antes de executar
- ✅ **Ambientes separados**: Teste e produção são completamente independentes
- ✅ **Logs detalhados**: Mostra exatamente o que está sendo executado

### Troubleshooting

#### Erro: "ModuleNotFoundError: No module named 'dotenv'"

```bash
pip install python-dotenv
```

#### Erro: "Connection refused"

- Verifique se o MySQL está rodando
- Confirme as credenciais no arquivo `.env`
- Teste a conexão manualmente

#### Erro: "Database does not exist"

- Crie o banco de dados antes de executar as migrações
- Verifique o nome do banco no arquivo `.env`

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

## 🔐 Sistema de Autenticação

### JWT (JSON Web Tokens)

- **Algoritmo**: HS256
- **Expiração**: Configurável via `JWT_EXPIRATION_TIME`
- **Refresh Tokens**: Implementados para renovação automática

### Criptografia de Senhas

- **Algoritmo**: bcrypt
- **Salt**: Gerado automaticamente
- **Rounds**: 12 (configurável)

### Exemplo de Implementação

```python
from src.auth.config.auth_secret_key import SecretKey
from src.auth.encrypt.encrypt import Encrypt

# Criptografar senha
encrypt = Encrypt()
hashed_password = encrypt.hash_password("senha123")

# Verificar senha
is_valid = encrypt.verify_password("senha123", hashed_password)
```

---

## 🗄️ Modelos de Dados

### Entidades Principais

#### Project

- **Tabela**: `project`
- **Campos**: id, status_id, name, verba_disponivel, andamento_do_projeto, start_date, expected_completion_date, end_date
- **Relacionamentos**: Status, HistoryProject, ProjectFiscal, ProjectBairro, ProjectEmpresa, ProjectType, UserProject, WorkProject

#### Fiscal

- **Tabela**: `fiscal`
- **Campos**: id, name, email, phone, password, salt, refresh_token, created_at
- **Relacionamentos**: ProjectFiscal, WorkProject

#### User

- **Tabela**: `user`
- **Campos**: id, cpf, password, salt, role, email, name, created_at
- **Relacionamentos**: UserProject, RefreshToken

### Relacionamentos

```
Project ──┬── ProjectFiscal ── Fiscal
          ├── ProjectBairro ── Bairro
          ├── ProjectEmpresa ── Empresa
          ├── ProjectType ── Types
          ├── UserProject ── User
          └── WorkProject ── Fiscal
```

---

## 🔧 Ferramentas de Desenvolvimento

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pylint
        name: pylint
        entry: .venv/bin/pylint
        language: system
        types: [python]
        args: ["-rn", "-sn", "--rcfile=.pylintrc"]
```

### Linting e Formatação

```bash
# Pylint
uv run pylint src/

# Black (formatação)
uv run black src/

# isort (imports)
uv run isort src/

# Type checking
uv run mypy src/
```

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

---

## 🚢 Deploy

### Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instalar UV
RUN pip install uv

# Copiar dependências
COPY pyproject.toml uv.lock ./
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

### Ambientes

1. **Desenvolvimento**: Local com hot-reload
2. **Homologação**: Ambiente de testes
3. **Produção**: Ambiente final

### Configurações por Ambiente

```env
# Desenvolvimento
HOMOLOGACAO=True
DEBUG=True
LOG_LEVEL=DEBUG

# Produção
HOMOLOGACAO=False
DEBUG=False
LOG_LEVEL=WARNING
```

---

## 📊 Monitoramento

### Logs

O sistema usa logging estruturado com diferentes níveis:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Operação realizada com sucesso")
logger.error("Erro na operação", exc_info=True)
```

### Métricas

- **Rate Limiting**: Proteção contra abuso
- **Health Checks**: Verificação de saúde da aplicação
- **Performance**: Monitoramento de tempo de resposta

---

## 🔒 Segurança

### Validação de Dados

- **Pydantic**: Validação automática de schemas
- **SQL Injection**: Prevenida pelo SQLAlchemy
- **XSS**: Sanitização de inputs

### Autenticação

- **JWT**: Tokens seguros
- **bcrypt**: Senhas criptografadas
- **Rate Limiting**: Proteção contra ataques

### CORS

```python
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Debugging

### Logs de Desenvolvimento

```python
# Ativar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debugger

```python
import pdb; pdb.set_trace()  # Python debugger
```

### FastAPI Debug

```bash
uvicorn main:app --reload --log-level debug
```

---

## 📚 Recursos Adicionais

### Documentação

- **OpenAPI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Este guia**: README.md

### Comunidade

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://pydantic-docs.helpmanual.io/

---

## 🏢 Informações do Projeto

### Propriedade

Este é um projeto privado desenvolvido para o Gabinete de Projetos. Todo o código e documentação são propriedade exclusiva de Alberto da Silva Mercado.

### Acesso

- **Repositório**: Acesso restrito apenas para membros autorizados
- **Documentação**: Interna e confidencial
- **Deploy**: Ambientes controlados e seguros

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
