#!/usr/bin/env python3
"""
Teste para verificar o endpoint de inserção de fiscal com todos os dados.
"""

import requests

# Configurações
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/auth/login"
INSERT_FISCAL_URL = f"{BASE_URL}/fiscal/insert-all"

def test_insert_all_fiscal_api():
    """
    Testa o fluxo de inserção de fiscal com todos os dados.
    """
    print("🧪 Testando Insert All Fiscal API")
    print("=" * 50)
    
    # Dados de teste para login de ADMIN
    admin_login_data = {
        "cpf": "123.456.789-00",  # Substitua por CPF de um ADMIN real
        "password": "senha123"
    }
    
    # Dados de teste para inserir fiscal
    fiscal_data = {
        "name": "João Silva Fiscal",
        "email": "joao.fiscal@teste.com",
        "password": "senha123",
        "phone": "(11) 99999-9999"
    }
    
    try:
        # 1. Login como ADMIN
        print("1. Fazendo login como ADMIN...")
        login_response = requests.post(LOGIN_URL, json=admin_login_data, timeout=10)
        
        if login_response.status_code != 200:
            print(f"❌ Erro no login do ADMIN: {login_response.status_code}")
            print(f"   Resposta: {login_response.text}")
            return
            
        login_result = login_response.json()
        token = login_result.get('token')
        print("✅ Login do ADMIN bem-sucedido!")
        print(f"   Token: {token[:50]}...")
        
        # 2. Inserir fiscal com todos os dados
        print("\n2. Inserindo fiscal com todos os dados...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        insert_response = requests.post(INSERT_FISCAL_URL, json=fiscal_data, headers=headers, timeout=10)
        
        if insert_response.status_code == 201:
            insert_result = insert_response.json()
            print("✅ Fiscal inserido com sucesso!")
            print(f"   Mensagem: {insert_result.get('message', 'N/A')}")
            print(f"   Status Code: {insert_response.status_code}")
        else:
            print(f"❌ Erro na inserção do fiscal: {insert_response.status_code}")
            print(f"   Resposta: {insert_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    test_insert_all_fiscal_api()
    print("\n" + "=" * 50)
    print("🏁 Teste concluído!")
    print("\n💡 Para testar no Swagger:")
    print("   1. Acesse: http://localhost:8000/docs")
    print("   2. Procure pela seção 'fiscal'")
    print("   3. Teste o endpoint 'POST /fiscal/insert-all'")
    print("   4. Lembre-se de fazer login como ADMIN primeiro!") 