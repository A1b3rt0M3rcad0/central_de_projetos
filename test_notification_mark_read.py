#!/usr/bin/env python3
"""
Script de teste para verificar se o endpoint de marcar notificação como lida está funcionando
"""

import requests
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:8000"
TEST_CPF = "12345678901"  # Substitua por um CPF válido do seu sistema
REQUEST_TIMEOUT = 30  # Timeout para requisições HTTP

def _get_notifications():
    """Busca notificações do usuário"""
    response = requests.get(
        f"{BASE_URL}/notification/find",
        params={
            "recipient_cpf": TEST_CPF,
            "limit": 5
        },
        headers={
            "Authorization": "Bearer YOUR_TOKEN_HERE"  # Substitua por um token válido
        },
        timeout=REQUEST_TIMEOUT
    )
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar notificações: {response.status_code}")
        print(f"   Resposta: {response.text}")
        return None
    
    data = response.json()
    notifications = data.get("notifications", [])
    
    if not notifications:
        print("❌ Nenhuma notificação encontrada para o CPF fornecido")
        return None
    
    return notifications


def _mark_notification_as_read(notification_id):
    """Marca uma notificação como lida"""
    mark_response = requests.post(
        f"{BASE_URL}/notification/mark_as_read",
        params={
            "notification_id": notification_id
        },
        headers={
            "Authorization": "Bearer YOUR_TOKEN_HERE"  # Substitua por um token válido
        },
        timeout=REQUEST_TIMEOUT
    )
    
    if mark_response.status_code != 200:
        print(f"❌ Erro ao marcar notificação como lida: {mark_response.status_code}")
        print(f"   Resposta: {mark_response.text}")
        return False
    
    print("✅ Notificação marcada como lida com sucesso!")
    return True


def _verify_notification_read(notification_id):
    """Verifica se a notificação foi marcada como lida"""
    verify_response = requests.get(
        f"{BASE_URL}/notification/find",
        params={
            "recipient_cpf": TEST_CPF,
            "limit": 5
        },
        headers={
            "Authorization": "Bearer YOUR_TOKEN_HERE"  # Substitua por um token válido
        },
        timeout=REQUEST_TIMEOUT
    )
    
    if verify_response.status_code != 200:
        print(f"❌ Erro ao verificar notificação: {verify_response.status_code}")
        print(f"   Resposta: {verify_response.text}")
        return False
    
    verify_data = verify_response.json()
    updated_notifications = verify_data.get("notifications", [])
    
    # Encontrar a notificação atualizada
    updated_notification = next(
        (n for n in updated_notifications if n.get("notification_id") == notification_id),
        None
    )
    
    if not updated_notification:
        print("❌ Não foi possível encontrar a notificação atualizada!")
        return False
    
    is_read = updated_notification.get("is_read")
    read_at = updated_notification.get("read_at")
    
    if is_read:
        print("✅ Notificação marcada como lida com sucesso!")
        print(f"   Data de leitura: {read_at}")
        return True
    
    print("❌ Notificação NÃO foi marcada como lida!")
    return False


def test_mark_notification_as_read():
    """Testa o endpoint de marcar notificação como lida"""
    
    print("🧪 Testando endpoint de marcar notificação como lida...")
    
    try:
        # 1. Buscar notificações
        print("\n1. Buscando notificações...")
        notifications = _get_notifications()
        if not notifications:
            return
        
        notification = notifications[0]
        notification_id = notification.get("notification_id")
        print(f"✅ Encontrada notificação com ID: {notification_id}")
        print(f"   Status atual: {'Lida' if notification.get('is_read') else 'Não lida'}")
        
        # 2. Marcar como lida
        print(f"\n2. Marcando notificação {notification_id} como lida...")
        if not _mark_notification_as_read(notification_id):
            return
        
        # 3. Verificar se foi marcada
        print("\n3. Verificando se a notificação foi marcada como lida...")
        _verify_notification_read(notification_id)
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Verifique se o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

def test_endpoint_structure():
    """Testa a estrutura do endpoint"""
    print("\n🔍 Testando estrutura do endpoint...")
    
    try:
        # Testar sem notification_id
        response = requests.post(
            f"{BASE_URL}/notification/mark_as_read",
            headers={
                "Authorization": "Bearer YOUR_TOKEN_HERE"
            },
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 400:
            print("✅ Endpoint retorna erro 400 quando notification_id não é fornecido")
        else:
            print(f"❌ Endpoint deveria retornar erro 400, mas retornou: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar estrutura: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando testes de notificação...")
    print(f"📍 URL base: {BASE_URL}")
    print(f"👤 CPF de teste: {TEST_CPF}")
    print("\n⚠️  IMPORTANTE: Configure um token válido e CPF existente antes de executar!")
    
    # test_endpoint_structure()
    # test_mark_notification_as_read()
    
    print("\n📝 Para executar os testes:")
    print("1. Configure um token válido no script")
    print("2. Configure um CPF válido que tenha notificações")
    print("3. Descomente as chamadas de teste no final do script")
    print("4. Execute: python test_notification_mark_read.py")
