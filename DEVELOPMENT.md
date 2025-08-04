# 🛠️ Guia de Desenvolvimento - Central de Projetos

## 📋 Visão Geral

Este documento contém informações técnicas detalhadas para desenvolvedores que trabalham no projeto Central de Projetos.

---

## 🏗️ Arquitetura do Sistema

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

#### WorkProject

- **Tabela**: `work_projects`
- **Campos**: id, project_id, fiscal_id, title, description, photo_name, created_at, updated_at
- **Relacionamentos**: Project, Fiscal

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

## 🧪 Testes

### Estrutura de Testes

```
src/
├── infra/relational/repository/_test/     # Testes de repositórios
├── data/use_cases/_tests/                 # Testes de casos de uso
├── presentation/controllers/_tests/        # Testes de controllers
└── main/composers/_tests/                 # Testes de integração
```

### Tipos de Testes

1. **Testes Unitários**: Testes isolados de componentes
2. **Testes de Integração**: Testes com banco de dados real
3. **Testes de API**: Testes end-to-end das rotas

### Executando Testes

```bash
# Todos os testes
pytest

# Testes específicos
pytest src/infra/relational/repository/_test/

# Com cobertura
pytest --cov=src --cov-report=html

# Testes paralelos
pytest -n auto
```

### Configuração de Testes

- **Banco de Teste**: `test_central_de_projetos`
- **Transações**: Revertidas após cada teste
- **Fixtures**: Reutilizáveis entre testes

---

## 🔄 Migrações

### Alembic

O projeto usa Alembic para controle de versão do banco de dados.

### Comandos Úteis

```bash
# Criar nova migração
alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1

# Ver histórico
alembic history
```

### Boas Práticas

1. **Sempre** gere migrações para mudanças no modelo
2. **Teste** as migrações em ambiente de desenvolvimento
3. **Documente** mudanças complexas
4. **Faça backup** antes de aplicar em produção

---

## 🚀 Deploy

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

### Linting

```bash
# Pylint
uv run pylint src/

# Black (formatação)
uv run black src/

# isort (imports)
uv run isort src/
```

### Type Checking

```bash
# mypy
uv run mypy src/
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
- **Este guia**: DEVELOPMENT.md

### Comunidade

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://pydantic-docs.helpmanual.io/

---

## 👨‍💻 Desenvolvedor

**Alberto da Silva Mercado**

- **Email**: alberto.zimba2013@gmail.com
- **Telefone**: (48) 99162-3022

Este projeto foi desenvolvido integralmente por Alberto da Silva Mercado.
