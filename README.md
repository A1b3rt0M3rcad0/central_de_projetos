# 🏛 Central de Projetos – Gabinete de Projetos

## 📌 Visão Geral
Sistema interno para gestão de projetos legislativos municipais.
Permite o acompanhamento de:
- Andamento de cada projeto
- Verba disponível
- Data de início, estimada de conclusão e de finalização
- Status dos projetos
- Tipos de projetos
- Responsáveis (vereadores, fiscais, empresas envolvidas)

Além de facilitar o acesso aos documentos de cada projeto para vereadores e assessores.

## 🎯 Objetivo
Facilitar o controle e a transparência dos projetos pelo gabinete, com foco em eficiência e acessibilidade às informações de andamento e documentação.

---

## 🚀 Tecnologias

- **Linguagem**: Python 3.12+
- **Framework**: FastAPI (para rotas e controllers)
- **Arquitetura**: Arquitetura limpa (Domain-Use Cases-Controllers-Repositories)
- **Banco de Dados**: MySQL (via SQLAlchemy)
- **Ambiente/Dependências**: Astral UV (gerenciador de venv e lockfile)
- **Testes**: pytest (cobertura principalmente nos repositórios)
- **Documentação**: OpenAPI (gerada automaticamente pelo FastAPI)

---

## 📦 Estrutura de Pastas

```plain
├── src/
│   ├── auth/        # Authenticação e regras de autenticação do sistema
│   ├── data/        # Interfaces dos repositorios e implementação dos casos de uso
│   ├── domain/      # Regras puras de negócio e objetos de valor do sistema
│   ├── errors/      # Erros persoalizados do sistema
│   ├── infra/       # Implementação dos repositorios e do banco de dados
|   ├── main/        # Aplicação completa com FastAPI
|   ├── presentaion/ # Implemantação dos controllers
|   ├── secutiry/    # Securança de dados
````

## ⚙️ Configurando o Ambiente

### 1. Instalando o UV

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Inicializando o Projeto

```shell
uv init
```

### 3. Instalando Dependências

```shell
uv sync
```

### 4. Ativando o Ambiente

* **macOS/Linux**

  ```shell
  source .venv/bin/activate
  ```
* **Windows (PowerShell)**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

---

## ▶️ Executando a API

com ambiente ativo

```shell
uvicorn src.main:app --reload
```

Acesse a documentação interativa em:

```
http://127.0.0.1:8000/docs
```

---

## ✅ Testes

Com ambiente já ativo e as configurações de ambiente ja configuradas

```shell
pytest
```

---

## 🚢 Deploy

1. **Docker**

   * Crie um `Dockerfile` com base em Python 3.12+.
   * Copie o projeto e instale dependências usando `uv sync --no-dev`.
   * Exponha a porta 8000.
2. **CI/CD**

   * Pipelines (GitHub Actions, GitLab CI, Jenkins) devem executar:

     ```shell
     uv sync
     pytest --cov
     docker build -t central-de-projetos .
     docker push <registry>/central-de-projetos:latest
     ```
3. **Produção**

   * Use AWS ECS, GCP Cloud Run ou Heroku apontando para a imagem Docker.
