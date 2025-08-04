# Migration Manager

Script para gerenciar migrações Alembic em múltiplos ambientes (teste e produção) usando variáveis de ambiente.

## 🚀 Como usar

### 1. Configuração das variáveis de ambiente

O script usa as variáveis do arquivo `.env` baseado no `.env.example`:

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

### 2. Comandos disponíveis

#### Upgrade para a versão mais recente

```bash
# Apenas banco de teste
python migration_manager.py upgrade head --test

# Apenas banco de produção
python migration_manager.py upgrade head --prod

# Ambos os bancos
python migration_manager.py upgrade head --all
```

#### Downgrade para uma versão específica

```bash
# Downgrade no banco de teste
python migration_manager.py downgrade 81f36764d1ba --test

# Downgrade em ambos os bancos
python migration_manager.py downgrade 81f36764d1ba --all
```

#### Verificar versão atual

```bash
# Verificar versão no banco de produção
python migration_manager.py current --prod

# Verificar versão em ambos os bancos
python migration_manager.py current --all
```

#### Ver histórico de migrações

```bash
# Histórico no banco de teste
python migration_manager.py history --test

# Histórico em ambos os bancos
python migration_manager.py history --all
```

### 3. Exemplos práticos

```bash
# Aplicar todas as migrações pendentes em ambos os bancos
python migration_manager.py upgrade head --all

# Voltar uma versão em ambos os bancos
python migration_manager.py downgrade -1 --all

# Verificar status atual em ambos os bancos
python migration_manager.py current --all

# Ver histórico completo em ambos os bancos
python migration_manager.py history --all
```

### 4. Todos os comandos Alembic suportados

O script aceita **qualquer comando** do Alembic diretamente. Aqui estão todos os comandos disponíveis:

#### Comandos básicos

```bash
# Upgrade/Downgrade
python migration_manager.py upgrade head --all
python migration_manager.py upgrade -1 --all
python migration_manager.py upgrade +1 --all
python migration_manager.py upgrade 558b6dc0169e --all

python migration_manager.py downgrade head --all
python migration_manager.py downgrade -1 --all
python migration_manager.py downgrade +1 --all
python migration_manager.py downgrade 81f36764d1ba --all

# Informações
python migration_manager.py current --all
python migration_manager.py history --all
python migration_manager.py show 558b6dc0169e --all
```

#### Comandos de criação de migrações

```bash
# Migração automática (detecta mudanças no modelo)
python migration_manager.py revision --autogenerate -m "descrição da migração" --all

# Migração vazia (para comandos SQL manuais)
python migration_manager.py revision -m "migração manual" --all

# Mesclar branches de migração
python migration_manager.py merge heads --all
```

#### Comandos de controle

```bash
# Marcar versão como aplicada sem executar
python migration_manager.py stamp head --all
python migration_manager.py stamp 558b6dc0169e --all

# Verificar diferenças
python migration_manager.py check --all
```

## 🔒 Segurança

- ✅ **Sem senhas no código**: Todas as credenciais vêm do arquivo `.env`
- ✅ **Confirmação**: O script sempre pede confirmação antes de executar
- ✅ **Ambientes separados**: Teste e produção são completamente independentes
- ✅ **Logs detalhados**: Mostra exatamente o que está sendo executado

## 📋 Funcionalidades

- 🎯 **Múltiplos ambientes**: Execute em teste, produção ou ambos
- 🔄 **Todos os comandos Alembic**: O script aceita **qualquer comando** do Alembic diretamente
- ✅ **Confirmação de segurança**: Sempre pede confirmação antes de executar
- 📊 **Relatório de sucesso**: Mostra quantas operações foram bem-sucedidas
- 🛡️ **Tratamento de erros**: Captura e exibe erros de forma clara

## ⚠️ Importante

- **Sempre faça backup** antes de executar migrações em produção
- **Teste primeiro** no banco de teste antes de aplicar em produção
- **Verifique** o comando antes de confirmar a execução
- **Mantenha** o arquivo `.env` seguro e nunca o commite no Git

## 🆘 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'dotenv'"

```bash
pip install python-dotenv
```

### Erro: "Connection refused"

- Verifique se o MySQL está rodando
- Confirme as credenciais no arquivo `.env`
- Teste a conexão manualmente

### Erro: "Database does not exist"

- Crie o banco de dados antes de executar as migrações
- Verifique o nome do banco no arquivo `.env`
