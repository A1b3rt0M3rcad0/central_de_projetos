import jwt
from src.auth.encrypt.interface.i_encrypt import IEncrypt
from src.auth.config.interface.i_auth_algoritm import IAuthAlgoritm
from src.auth.config.interface.i_auth_secret_key import IAuthSecretKey

class Encrypt(IEncrypt):

    def __init__(self, algoritm: IAuthAlgoritm, secret_key: IAuthSecretKey) -> None:
        self.__algoritm = algoritm.algoritm
        self.__secret_key = secret_key.secret_key

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self.__secret_key, self.__algoritm)
    
    def decode(self, token: str) -> dict:
        return jwt.decode(token, self.__secret_key, self.__algoritm)