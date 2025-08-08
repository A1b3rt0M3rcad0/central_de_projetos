# Implementação da Rota Mobile para Criação de Work Project

## Visão Geral

Foi implementada uma nova rota mobile para criação de work projects, exclusiva para fiscais autenticados. A funcionalidade inclui validação de vínculo entre fiscal e projeto, garantindo que apenas fiscais vinculados ao projeto possam criar work projects.

## Funcionalidades Implementadas

### 1. Controller Mobile (`CreateWorkProjectMobileController`)

- **Localização**: `src/presentation/controllers/create_work_project_mobile_controller.py`
- **Responsabilidades**:
  - Validação de vínculo fiscal-projeto
  - Processamento de documentos fiscais
  - Criação do work project
  - Salvamento de documentos no RavenDB
  - Criação de histórico do projeto

### 2. Composer Mobile (`create_work_project_mobile_composer`)

- **Localização**: `src/main/composers/create_work_project_mobile_composer.py`
- **Responsabilidades**:
  - Injeção de dependências
  - Configuração de conexões com bancos de dados
  - Criação do controller com todas as dependências necessárias

### 3. Rota Mobile

- **Localização**: `src/main/routes/mobile/fiscal/fiscal_mobile_routes.py`
- **Endpoint**: `POST /mobile/fiscal/create_work_project`
- **Autenticação**: Requer token JWT de fiscal
- **Validação**: Verifica se o fiscal está vinculado ao projeto

### 4. Formato de Resposta

- **Localização**: `src/main/routes/mobile/fiscal/response_format/create_work_project_response.py`
- **Campos**:
  - `message`: Mensagem de sucesso
  - `work_project_id`: ID do work project criado
  - `title`: Título do work project
  - `photo_name`: Nome da foto (opcional)
  - `documents_count`: Quantidade de documentos

### 5. Erro de Autorização

- **Localização**: `src/errors/use_cases/fiscal_not_authorized_error.py`
- **Uso**: Lançado quando fiscal não está vinculado ao projeto

## Validações Implementadas

### 1. Autenticação de Fiscal

- Token JWT obrigatório
- Role deve ser "fiscal"
- Middleware `fiscal_required()` aplicado

### 2. Vínculo Fiscal-Projeto

- Verifica se existe associação na tabela `project_fiscal`
- Se não existir, retorna erro `FiscalNotAuthorizedError`
- Mensagem: "Fiscal {fiscal_id} não está autorizado a criar work project para o projeto {project_id}. Fiscal deve estar vinculado ao projeto."

### 3. Processamento de Documentos

- Suporte a múltiplos arquivos
- Detecção automática de imagem para `photo_name`
- Salvamento no RavenDB
- Lista de documentos em JSON

## Como Usar

### 1. Autenticação

```bash
# Login do fiscal
POST /mobile/fiscal/login
{
  "email": "fiscal@example.com",
  "password": "senha123"
}
```

### 2. Criação de Work Project

```bash
# Criar work project
POST /mobile/fiscal/create_work_project
Authorization: Bearer {token_jwt}
Content-Type: multipart/form-data

Form Data:
- project_id: 1
- title: "Título do Work Project"
- description: "Descrição do Work Project"
- files: [arquivos opcionais]
```

### 3. Resposta de Sucesso

```json
{
  "message": "Work project created successfully via mobile",
  "work_project_id": 123,
  "title": "Título do Work Project",
  "photo_name": "imagem.jpg",
  "documents_count": 2
}
```

### 4. Resposta de Erro (Fiscal não vinculado)

```json
{
  "error": "FiscalNotAuthorizedError",
  "message": "Fiscal 1 não está autorizado a criar work project para o projeto 999. Fiscal deve estar vinculado ao projeto."
}
```

## Estrutura de Dados

### Work Project

```sql
CREATE TABLE work_projects (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES project(id),
    fiscal_id INTEGER REFERENCES fiscal(id),
    title VARCHAR(255),
    description VARCHAR(500),
    photo_name VARCHAR(255),
    additional_documents JSON,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Project Fiscal (Vínculo)

```sql
CREATE TABLE project_fiscal (
    fiscal_id INTEGER REFERENCES fiscal(id),
    project_id INTEGER REFERENCES project(id),
    created_at DATETIME,
    PRIMARY KEY (fiscal_id, project_id)
);
```

## Testes Implementados

### 1. Testes Unitários

- **Arquivo**: `src/main/composers/_tests/create_work_project_mobile_composer_test.py`
- **Cobertura**: Composer, dependências, imports

### 2. Testes de Integração

- **Arquivo**: `src/main/composers/_tests/create_work_project_mobile_integration_test.py`
- **Cobertura**: Validação de fiscal, documentos, histórico

## Fluxo de Execução

1. **Recebimento da Requisição**

   - Validação do token JWT
   - Extração dos dados do formulário

2. **Validação de Autorização**

   - Verifica se fiscal está vinculado ao projeto
   - Se não estiver, retorna erro

3. **Processamento de Documentos**

   - Processa arquivos enviados
   - Identifica imagem para foto
   - Prepara lista de documentos

4. **Criação do Work Project**

   - Insere na tabela `work_projects`
   - Salva documentos no RavenDB
   - Cria histórico do projeto

5. **Resposta**
   - Retorna dados do work project criado
   - Inclui contagem de documentos

## Segurança

- **Autenticação**: Token JWT obrigatório
- **Autorização**: Apenas fiscais podem acessar
- **Validação**: Fiscal deve estar vinculado ao projeto
- **Logs**: Todas as operações são logadas

## Banco de Dados

### Relational Database (MySQL)

- Tabela `work_projects`: Dados principais
- Tabela `project_fiscal`: Vínculo fiscal-projeto
- Tabela `history_project`: Histórico de alterações

### RavenDB

- Documentos fiscais associados ao work project
- Estrutura: `ProjectDocumentsFiscal/{work_project_id}`

## Considerações Técnicas

1. **Clean Architecture**: Seguindo os princípios do projeto
2. **Dependency Injection**: Composer injeta todas as dependências
3. **Error Handling**: Tratamento específico para cada tipo de erro
4. **Logging**: Logs detalhados para auditoria
5. **Testing**: Testes unitários e de integração
6. **Documentation**: Documentação completa da API
