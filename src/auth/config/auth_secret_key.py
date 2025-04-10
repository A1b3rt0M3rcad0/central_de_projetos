import os
import dotenv
from src.auth.config.interface.i_auth_secret_key import IAuthSecretKey

class AuthSecretKey(IAuthSecretKey):

    def __init__(self) -> None:
        self.__secret_key = self._get_secret_key()
    
    @property
    def secret_key(self) -> str:
        return self.__secret_key

    def _get_secret_key(self) -> str:
        dotenv.load_dotenv()
        secret_key = os.getenv("SECRET_KEY")
        return secret_key if secret_key else None