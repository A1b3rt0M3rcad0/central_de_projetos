# Dockerfile para Central de Projetos (Backend)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Definir variáveis de ambiente para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências usando uv
RUN uv sync --frozen --no-dev

# Copiar o código da aplicação
COPY . .

# Expor a porta da aplicação
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

