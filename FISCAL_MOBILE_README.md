# Fiscal Mobile API

Este documento descreve a implementação do middleware de autorização e rotas específicas para fiscais mobile.

## 📁 Estrutura de Arquivos

```
src/main/routes/
├── middleware/
│   └── fiscal_authorization.py          # Middleware específico para fiscais
└── mobile/
    └── fiscal/
        ├── fiscal_mobile_routes.py      # Rotas mobile dos fiscais
        ├── request_format/
        │   └── login_fiscal_format.py   # Formato de requisição de login
        └── response_format/
            ├── login_fiscal_response.py # Resposta de login
            └── test_fiscal_response.py  # Resposta de teste
```

## 🔐 Middleware de Autorização

### `fiscal_authorization.py`

O middleware `fiscal_authorization.py` foi criado especificamente para autenticação de fiscais mobile, baseado no middleware de autorização geral mas com validações específicas para o role `FISCAL`.

#### Funcionalidades:

1. **Validação de Token JWT**: Verifica se o token é válido e não expirou
2. **Verificação de Role**: Garante que apenas usuários com role `FISCAL` podem acessar
3. **Renovação Automática**: Renova tokens expirados usando refresh tokens
4. **Injeção de Dados**: Injetar dados do fiscal no `request.state.fiscal`

#### Funções Principais:

- `get_current_fiscal()`: Valida o token e verifica se o usuário é fiscal
- `fiscal_required()`: Dependência para rotas que requerem autenticação de fiscal

## 🛣️ Rotas Mobile

### Endpoints Disponíveis

#### 1. Login do Fiscal

```
POST /mobile/fiscal/login
```

**Request Body:**

```json
{
  "email": "fiscal@exemplo.com",
  "password": "senha123"
}
```

**Response:**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "Login realizado com sucesso"
}
```

#### 2. Teste de Autenticação

```
GET /mobile/fiscal/test
```

**Headers:**

```
Authorization: Bearer <token_jwt>
```

**Response:**

```json
{
  "message": "Fiscal autenticado com sucesso!",
  "fiscal_email": "fiscal@exemplo.com",
  "fiscal_role": "fiscal",
  "timestamp": "2024-01-15T10:30:00.123456",
  "status": "success"
}
```

## 🔧 Como Usar

### 1. Importar o Middleware

```python
from src.main.routes.middleware.fiscal_authorization import fiscal_required
```

### 2. Aplicar em Rotas

```python
@routes.get('/protegida')
async def rota_protegida(
    request: Request,
    fiscal: dict = Security(fiscal_required())
):
        # Acesso aos dados do fiscal
    fiscal_data = request.state.fiscal
    email = fiscal_data.get("email")

    return {"message": f"Olá fiscal {email}!"}
```

### 3. Acessar Dados do Fiscal

```python
# No controller ou rota
fiscal_data = request.state.fiscal
email = fiscal_data.get("email")
role = fiscal_data.get("role")
```

## 🧪 Testando

### Executar Teste Automático

```bash
python test_fiscal_mobile.py
```

### Teste Manual com curl

1. **Login:**

```bash
curl -X POST "http://localhost:8000/mobile/fiscal/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "fiscal@exemplo.com", "password": "senha123"}'
```

2. **Teste com Token:**

```bash
curl -X GET "http://localhost:8000/mobile/fiscal/test" \
     -H "Authorization: Bearer <token_obtido_no_login>"
```

## 🚨 Tratamento de Erros

### Códigos de Status HTTP

- `200`: Sucesso
- `401`: Token não encontrado ou inválido
- `403`: Acesso negado (usuário não é fiscal)
- `500`: Erro interno do servidor

### Mensagens de Erro

- "Token não encontrado."
- "Token inválido."
- "Acesso negado. Apenas fiscais podem acessar este recurso."
- "Refresh token não encontrado. Faça login novamente."
- "Refresh token expirado. Faça login novamente."

## 🔄 Renovação de Token

O middleware automaticamente renova tokens expirados usando refresh tokens, mantendo a sessão do usuário ativa sem necessidade de novo login.

## 📝 Notas Importantes

1. **Segurança**: O middleware verifica especificamente o role `FISCAL`
2. **Performance**: Tokens são validados e renovados automaticamente
3. **Logs**: Todas as operações são logadas para auditoria
4. **Compatibilidade**: Funciona com o sistema de refresh tokens existente

## 🔗 Integração

As rotas mobile dos fiscais estão integradas na aplicação principal em `src/main/app.py` e são acessíveis através do prefixo `/mobile/fiscal`.
