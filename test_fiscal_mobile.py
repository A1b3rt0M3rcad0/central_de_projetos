#!/usr/bin/env python3
"""
Teste simples para verificar o middleware e rota de teste dos fiscais mobile.
"""

import requests

# Configurações
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/mobile/fiscal/login"
TEST_URL = f"{BASE_URL}/mobile/fiscal/test"

def test_fiscal_mobile():
    """
    Testa o fluxo completo de login e teste do fiscal mobile.
    """
    print("🧪 Testando Fiscal Mobile API")
    print("=" * 50)
    
    # Dados de teste (substitua por dados reais de um fiscal)
    login_data = {
        "email": "fiscal@teste.com",
        "password": "senha123"
    }
    
    try:
        # 1. Teste de login
        print("1. Testando login do fiscal...")
        login_response = requests.post(LOGIN_URL, json=login_data, timeout=10)
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            print("✅ Login bem-sucedido!")
            print(f"   Token: {login_result.get('token', 'N/A')[:50]}...")
            
            # 2. Teste da rota protegida
            print("\n2. Testando rota protegida...")
            headers = {
                "Authorization": f"Bearer {login_result.get('token')}",
                "Content-Type": "application/json"
            }
            
            test_response = requests.get(TEST_URL, headers=headers, timeout=10)
            
            if test_response.status_code == 200:
                test_result = test_response.json()
                print("✅ Rota de teste acessada com sucesso!")
                print(f"   Email do fiscal: {test_result.get('fiscal_email')}")
                print(f"   Role: {test_result.get('fiscal_role')}")
                print(f"   Mensagem: {test_result.get('message')}")
                print(f"   Timestamp: {test_result.get('timestamp')}")
            else:
                print(f"❌ Erro ao acessar rota de teste: {test_response.status_code}")
                print(f"   Resposta: {test_response.text}")
                
        else:
            print(f"❌ Erro no login: {login_response.status_code}")
            print(f"   Resposta: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

def test_without_token():
    """
    Testa a rota protegida sem token para verificar se o middleware está funcionando.
    """
    print("\n3. Testando acesso sem token...")
    
    try:
        response = requests.get(TEST_URL, timeout=10)
        
        if response.status_code == 401:
            print("✅ Middleware funcionando corretamente - acesso negado sem token")
        else:
            print(f"❌ Erro: deveria retornar 401, mas retornou {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar sem token: {str(e)}")

if __name__ == "__main__":
    test_fiscal_mobile()
    test_without_token()
    print("\n" + "=" * 50)
    print("�� Teste concluído!") 