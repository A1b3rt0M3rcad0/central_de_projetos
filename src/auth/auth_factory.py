from src.auth.encrypt.encrypt import Encrypt
from src.auth.config.auth_algoritm import AuthAlgoritm
from src.auth.config.auth_secret_key import AuthSecretKey

def auth_factory() -> Encrypt:
    return Encrypt(AuthAlgoritm(), AuthSecretKey())