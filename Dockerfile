# ==============================================================================
# Dockerfile - Central de Projetos (Backend)
# ==============================================================================
# 
# Este Dockerfile cria uma imagem para o backend FastAPI com suporte a:
# - Python 3.12
# - FastAPI + SQLAlchemy
# - MySQL
# - Redis
# - UV (gerenciador de pacotes Python)
#
# USO:
#   Desenvolvimento:
#     docker build --target development -t central-projetos:dev .
#     docker run -p 8000:8000 --env-file .env central-projetos:dev
#
#   Produção:
#     docker build --target production -t central-projetos:prod .
#     docker run -p 8000:8000 --env-file .env central-projetos:prod
#
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage Base: Imagem base com Python 3.12 e UV
# ------------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim as base

# Instalar dependências do sistema necessárias
# - curl: para healthcheck
# - gcc: compilador C para algumas dependências Python
# - default-mysql-client: cliente MySQL
# - default-libmysqlclient-dev: bibliotecas de desenvolvimento MySQL
# - pkg-config: para configuração de pacotes
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    default-mysql-client \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Configurar variáveis de ambiente do Python
# PYTHONUNBUFFERED: desabilita buffer de saída (logs aparecem imediatamente)
# PYTHONDONTWRITEBYTECODE: evita criação de arquivos .pyc
# UV_SYSTEM_PYTHON: usa Python do sistema
# PYTHONPATH: define caminho para módulos Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    PYTHONPATH=/app

# Definir diretório de trabalho dentro do container
WORKDIR /app

# ------------------------------------------------------------------------------
# Stage 1: Dependencies - Instalação de dependências Python
# ------------------------------------------------------------------------------
FROM base as dependencies

# Copiar arquivos de configuração de dependências
# pyproject.toml: define dependências do projeto
# uv.lock: lock file com versões exatas (garante reprodutibilidade)
COPY pyproject.toml uv.lock ./

# Instalar todas as dependências do projeto
# --frozen: usa apenas versões do uv.lock (não atualiza dependências)
RUN uv sync --frozen

# ------------------------------------------------------------------------------
# Stage 2: Development - Ambiente de desenvolvimento
# ------------------------------------------------------------------------------
FROM dependencies as development

# Copiar todo o código da aplicação
# (em desenvolvimento, copiamos tudo para permitir hot-reload)
COPY . .

# Expor porta 8000 (porta padrão do FastAPI)
EXPOSE 8000

# Healthcheck: verifica se a aplicação está respondendo
# Interval: verifica a cada 30 segundos
# Timeout: timeout de 10 segundos por verificação
# Start-period: aguarda 40 segundos antes da primeira verificação
# Retries: tenta 3 vezes antes de marcar como não saudável
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Comando para iniciar a aplicação em modo desenvolvimento
# --reload: habilita hot-reload (reinicia automaticamente ao detectar mudanças)
# --host 0.0.0.0: permite acesso de qualquer IP
# --port 8000: porta da aplicação
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ------------------------------------------------------------------------------
# Stage 3: Production - Ambiente de produção
# ------------------------------------------------------------------------------
FROM dependencies as production

# Copiar código da aplicação
# (em produção, apenas código necessário)
COPY . .

# Criar usuário não-root para maior segurança
# -m: cria diretório home
# -u 1000: define UID 1000
# appuser: nome do usuário
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Mudar para usuário não-root (segurança)
# IMPORTANTE: Executa a aplicação sem privilégios de root
USER appuser

# Expor porta 8000
EXPOSE 8000

# Healthcheck (mesmo do desenvolvimento)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Comando para iniciar a aplicação em modo produção
# --workers 4: cria 4 processos worker (melhor performance)
# Sem --reload: não reinicia automaticamente (produção)
# 
# NOTA: Para produção, considere usar um process manager como:
# - Gunicorn com Uvicorn workers
# - Supervisor
# - Systemd
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# ==============================================================================
# VARIÁVEIS DE AMBIENTE NECESSÁRIAS
# ==============================================================================
# 
# Certifique-se de criar um arquivo .env com as seguintes variáveis:
# 
# OBRIGATÓRIAS:
#   - SECRET_KEY: Chave secreta para JWT
#   - DATABASE, DRIVE, USERNAME, PASSWORD, HOST, PORT, DATABASE_NAME: MySQL
#   - CORS_ORIGINS: URLs permitidas para CORS (em produção)
#
# OPCIONAIS:
#   - MONGO_HOST, MONGO_PORT, etc: MongoDB (logs)
#   - REDIS_URL, REDIS_PORT, etc: Redis (cache)
#   - RAVEN_URL, etc: RavenDB (documentos)
#
# Veja .env.example para mais detalhes
#
# ==============================================================================
