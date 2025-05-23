from src.domain.use_cases.i_valid_jwt import IValidJwt
from src.auth.encrypt.interface.i_encrypt import IEncrypt

class ValidJwt(IValidJwt):

    def __init__(self, encrypt:IEncrypt) -> None:
        self.__encrypt = encrypt
    
    def valid(self, token:str) -> dict:
        '''
        return {
            invalid: bool,
            expired: bool
        }
        '''
        try:
            result = self.__encrypt.is_expired(
                token=token
            )
            return result
        except Exception as e:
            raise e from e