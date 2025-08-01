# 🏛️ Insert All Fiscal API

## 📋 Descrição

Esta funcionalidade permite que **ADMINs** criem fiscais com todos os dados necessários (nome, email, senha, telefone) através da API.

## 🔐 Autenticação

- **Apenas ADMINs** podem acessar este endpoint
- Requer token JWT válido no header `Authorization: Bearer <token>`

## 🚀 Endpoint

### POST `/fiscal/insert-all`

**URL:** `http://localhost:8000/fiscal/insert-all`

**Método:** `POST`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body:**
```json
{
    "name": "João Silva Fiscal",
    "email": "joao.fiscal@exemplo.com",
    "password": "senha123",
    "phone": "(11) 99999-9999"
}
```

**Resposta de Sucesso (201):**
```json
{
    "message": "Fiscal inserted successfully"
}
```

**Resposta de Erro (400/401/403/500):**
```json
{
    "error": "Mensagem de erro específica"
}
```

## 📝 Campos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `name` | string | ✅ | Nome completo do fiscal |
| `email` | email | ✅ | Email único do fiscal |
| `password` | string | ✅ | Senha do fiscal (será hasheada) |
| `phone` | string | ✅ | Telefone do fiscal |

## 🔄 Fluxo de Uso

### 1. Login como ADMIN
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "123.456.789-00",
    "password": "senha123"
  }'
```

### 2. Inserir Fiscal
```bash
curl -X POST "http://localhost:8000/fiscal/insert-all" \
  -H "Authorization: Bearer <seu_token_jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva Fiscal",
    "email": "joao.fiscal@exemplo.com",
    "password": "senha123",
    "phone": "(11) 99999-9999"
  }'
```

## 🧪 Teste

Execute o script de teste:

```bash
python3 test_insert_all_fiscal_api.py
```

## 📚 Swagger

1. Acesse: `http://localhost:8000/docs`
2. Procure pela seção **"fiscal"**
3. Teste o endpoint **"POST /fiscal/insert-all"**
4. Lembre-se de fazer login como ADMIN primeiro!

## ⚠️ Observações

- O email deve ser único no sistema
- A senha será automaticamente hasheada usando Blowfish
- Apenas ADMINs podem criar fiscais
- O fiscal criado poderá fazer login usando email e senha

## 🔧 Arquivos Criados/Modificados

- ✅ `src/main/routes/api/fiscal/request_format/insert_all_fiscal_from_user_format.py` - Formato de requisição
- ✅ `src/main/routes/api/fiscal/fiscal_routes.py` - Nova rota adicionada
- ✅ `test_insert_all_fiscal_api.py` - Script de teste
- ✅ `INSERT_ALL_FISCAL_API_README.md` - Esta documentação

## 🏗️ Arquitetura

A implementação segue o padrão Clean Architecture do projeto:

```
Controller → Use Case → Repository → Database
```

- **Controller:** `InsertAllFiscalFromFiscalController`
- **Use Case:** `InsertAllFiscalFromFiscalUseCase`
- **Repository:** `FiscalRepository.insert_all_from_fiscal()`
- **Composer:** `insert_all_fiscal_from_user_composer()` 