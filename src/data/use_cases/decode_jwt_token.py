from src.domain.use_cases.i_decode_jwt_token import IDecodeJwtToken
from src.auth.encrypt.interface.i_encrypt import IEncrypt
from typing import Dict

class DecodeJwtToken(IDecodeJwtToken):

    def __init__(self, encrypt:IEncrypt) -> None:
        self.__encrypt = encrypt
    
    def decode(self, token:str, verify_exp=True) -> Dict:
        try:
            result = self.__encrypt.decode(
                token=token,
                verify_exp=verify_exp
            )
            return result
        except Exception as e:
            raise e from e