from src.domain.use_cases.i_encode_jwt import IEncodeJwt
from src.auth.encrypt.interface.i_encrypt import IEncrypt
from typing import Dict

class EncodeJwt(IEncodeJwt):

    def __init__(self, encrypt:IEncrypt) -> None:
        self.__encrypt = encrypt
    
    def encode(self, payload:Dict) -> str:
        try:
            token = self.__encrypt.encode(
                payload=payload
            )
            return token
        except Exception as e:
            raise e from e