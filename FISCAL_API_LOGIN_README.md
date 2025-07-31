# Fiscal API Login

Este documento descreve a implementação do endpoint de login do fiscal na API principal, permitindo que você faça login do fiscal no Swagger da mesma forma que faz com o user.

## 🛣️ Endpoints Disponíveis

### 1. Login de User (existente)
```
POST /auth/login
```

**Request Body:**
```json
{
  "cpf": "123.456.789-00",
  "password": "senha123"
}
```

### 2. Login de Fiscal (novo!)
```
POST /auth/login/fiscal
```

**Request Body:**
```json
{
  "email": "fiscal@exemplo.com",
  "password": "senha123"
}
```

### 📋 Resposta (ambos retornam o mesmo formato)
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 🔍 Como usar no Swagger

1. **Acesse o Swagger:**
   ```
   http://localhost:8000/docs
   ```

2. **Procure pela seção "auth":**
   - Você verá dois endpoints de login
   - `POST /auth/login` - para usuários (CPF)
   - `POST /auth/login/fiscal` - para fiscais (Email)

3. **Teste o endpoint:**
   - Clique em "Try it out"
   - Preencha os dados:
     - **Para user:** `cpf` e `password`
     - **Para fiscal:** `email` e `password`
   - Execute e receba o token JWT

## 📁 Arquivos Criados/Modificados

### Arquivos Criados:
- `src/main/routes/api/auth/request_format/login_fiscal_format.py` - Formato de requisição

### Arquivos Modificados:
- `src/main/routes/api/auth/login_routes.py` - Adicionado endpoint do fiscal

## ✅ Características do Endpoint

- ✅ **Mesma interface** no Swagger
- ✅ **Mesmo formato** de resposta
- ✅ **Mesmo sistema** de rate limiting (5/minuto)
- ✅ **Mesmo tratamento** de erros
- ✅ **Logs centralizados**
- ✅ **Validação Pydantic** com EmailStr

## 🧪 Testando

### Executar Teste Automático:
```bash
python3 test_fiscal_api_login.py
```

### Teste Manual com curl:

**Login do Fiscal:**
```bash
curl -X POST "http://localhost:8000/auth/login/fiscal" \
     -H "Content-Type: application/json" \
     -d '{"email": "fiscal@exemplo.com", "password": "senha123"}'
```

**Login do User (para comparação):**
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"cpf": "123.456.789-00", "password": "senha123"}'
```

## 🚨 Tratamento de Erros

### Códigos de Status HTTP:
- `200`: Sucesso
- `400`: Dados inválidos
- `401`: Credenciais inválidas
- `422`: Erro de validação (Pydantic)
- `500`: Erro interno do servidor

### Mensagens de Erro:
- "The fiscal with this email: {email} does not exists"
- "The password {password} is incorrect"
- "Invalid email format"

## 🔄 Integração

O endpoint está integrado na aplicação principal e é acessível através do prefixo `/auth/login/fiscal`. Ele usa o mesmo sistema de autenticação e refresh tokens que o login de user.

## 📝 Notas Importantes

1. **Segurança**: Usa o mesmo sistema de rate limiting (5 tentativas por minuto)
2. **Validação**: Email é validado usando EmailStr do Pydantic
3. **Compatibilidade**: Funciona com o sistema de refresh tokens existente
4. **Logs**: Todas as operações são logadas para auditoria
