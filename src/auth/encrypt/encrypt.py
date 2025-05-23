import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from src.auth.encrypt.interface.i_encrypt import IEncrypt
from src.auth.config.interface.i_auth_algoritm import IAuthAlgoritm
from src.auth.config.interface.i_auth_secret_key import IAuthSecretKey

class Encrypt(IEncrypt):

    def __init__(self, algoritm: IAuthAlgoritm, secret_key: IAuthSecretKey) -> None:
        self.__algoritm = algoritm.algoritm
        self.__secret_key = secret_key.secret_key

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self.__secret_key, self.__algoritm)
    
    def decode(self, token: str, verify_exp=True) -> dict:
        try:
            result = jwt.decode(token, self.__secret_key, self.__algoritm, options={'verify_exp':verify_exp})
            return result
        except ExpiredSignatureError:
            return {}
    
    def is_expired(self, token:str) -> dict:
        try:
            jwt.decode(token, self.__secret_key, self.__algoritm)
            return {
                'expired': False,
                'invalid': False
            }
        except ExpiredSignatureError:
            return {
                'expired': True,
                'invalid': False
            }
        except InvalidTokenError:
            return {
                'expired': False,
                'invalid': True
            }