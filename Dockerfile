# ==========================================================================
# Dockerfile para Central de Projetos (Backend - FastAPI + SQLAlchemy + Redis)
# ==========================================================================

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim as base

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    default-mysql-client \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Definir variáveis de ambiente para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    PYTHONPATH=/app

# Criar diretório de trabalho
WORKDIR /app

# ==========================================================================
# Stage 1: Dependencies
# ==========================================================================
FROM base as dependencies

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências (incluindo pymysql para MySQL)
RUN uv sync --frozen

# ==========================================================================
# Stage 2: Development
# ==========================================================================
FROM dependencies as development

# Copiar o código da aplicação
COPY . .

# Expor a porta da aplicação
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Comando para executar a aplicação em modo desenvolvimento
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ==========================================================================
# Stage 3: Production
# ==========================================================================
FROM dependencies as production

# Copiar apenas o código necessário
COPY . .

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor a porta da aplicação
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Comando para executar a aplicação em modo produção
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

