from src.auth.encrypt.encrypt import Encrypt
from src.auth.config.auth_algoritm import AuthAlgoritm
from src.auth.config.auth_secret_key import AuthSecretKey

def mocked_payload():
    return {"test": "test"}

def test_encode():
    encrypt = Encrypt(AuthAlgoritm(), AuthSecretKey())
    payload = mocked_payload()
    token = encrypt.encode(payload)
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

def test_decode():
    encrypt = Encrypt(AuthAlgoritm(), AuthSecretKey())
    payload = mocked_payload()
    token = encrypt.encode(payload)
    decoded = encrypt.decode(token)
    assert decoded is not None
    assert isinstance(decoded, dict)
    assert decoded["test"] == payload["test"]