#!/usr/bin/env python3
"""
Teste para verificar o endpoint de login do fiscal na API principal.
"""

import requests

# Configurações
BASE_URL = "http://localhost:8000"
LOGIN_USER_URL = f"{BASE_URL}/auth/login"
LOGIN_FISCAL_URL = f"{BASE_URL}/auth/login/fiscal"

def test_fiscal_api_login():
    """
    Testa o fluxo de login do fiscal na API principal.
    """
    print("🧪 Testando Fiscal API Login")
    print("=" * 50)
    
    # Dados de teste (substitua por dados reais de um fiscal)
    login_data = {
        "email": "fiscal@teste.com",
        "password": "senha123"
    }
    
    try:
        # Teste de login do fiscal
        print("1. Testando login do fiscal na API...")
        login_response = requests.post(LOGIN_FISCAL_URL, json=login_data, timeout=10)
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            print("✅ Login do fiscal bem-sucedido!")
            print(f"   Token: {login_result.get('token', 'N/A')[:50]}...")
            print(f"   Status Code: {login_response.status_code}")
        else:
            print(f"❌ Erro no login do fiscal: {login_response.status_code}")
            print(f"   Resposta: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

def test_user_api_login():
    """
    Testa o fluxo de login do user para comparação.
    """
    print("\n2. Testando login do user para comparação...")
    
    # Dados de teste (substitua por dados reais de um user)
    login_data = {
        "cpf": "123.456.789-00",
        "password": "senha123"
    }
    
    try:
        login_response = requests.post(LOGIN_USER_URL, json=login_data, timeout=10)
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            print("✅ Login do user bem-sucedido!")
            print(f"   Token: {login_result.get('token', 'N/A')[:50]}...")
            print(f"   Status Code: {login_response.status_code}")
        else:
            print(f"❌ Erro no login do user: {login_response.status_code}")
            print(f"   Resposta: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    test_fiscal_api_login()
    test_user_api_login()
    print("\n" + "=" * 50)
    print("🏁 Teste concluído!")
    print("\n💡 Para testar no Swagger:")
    print("   1. Acesse: http://localhost:8000/docs")
    print("   2. Procure pela seção 'auth'")
    print("   3. Teste o endpoint 'POST /auth/login/fiscal'")
