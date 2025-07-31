#!/usr/bin/env python3
"""
Teste para verificar se a correção da rota mobile dos fiscais funcionou.
"""

import requests

# Configurações
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/mobile/fiscal/login"
TEST_URL = f"{BASE_URL}/mobile/fiscal/test"

def test_fiscal_mobile_fix():
    """
    Testa se a correção da rota mobile funcionou.
    """
    print("🧪 Testando Correção da Rota Mobile Fiscal")
    print("=" * 50)
    
    # Dados de teste para login de fiscal
    login_data = {
        "email": "fiscal@teste.com",
        "password": "senha123"
    }
    
    try:
        # 1. Login do fiscal
        print("1. Fazendo login do fiscal...")
        login_response = requests.post(LOGIN_URL, json=login_data, timeout=10)
        
        if login_response.status_code != 200:
            print(f"❌ Erro no login do fiscal: {login_response.status_code}")
            print(f"   Resposta: {login_response.text}")
            return
            
        login_result = login_response.json()
        token = login_result.get('token')
        print("✅ Login do fiscal bem-sucedido!")
        print(f"   Token: {token[:50]}...")
        
        # 2. Testar rota protegida
        print("\n2. Testando rota protegida...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        test_response = requests.get(TEST_URL, headers=headers, timeout=10)
        
        if test_response.status_code == 200:
            test_result = test_response.json()
            print("✅ Rota de teste funcionando!")
            print(f"   Mensagem: {test_result.get('message', 'N/A')}")
            print(f"   Email: {test_result.get('fiscal_email', 'N/A')}")
            print(f"   Role: {test_result.get('fiscal_role', 'N/A')}")
            print(f"   Status Code: {test_response.status_code}")
        else:
            print(f"❌ Erro na rota de teste: {test_response.status_code}")
            print(f"   Resposta: {test_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    test_fiscal_mobile_fix()
    print("\n" + "=" * 50)
    print("�� Teste concluído!") 