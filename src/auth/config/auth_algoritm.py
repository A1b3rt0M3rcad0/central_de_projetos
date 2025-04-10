from src.auth.config.interface.i_auth_algoritm import IAuthAlgoritm

class AuthAlgoritm(IAuthAlgoritm):

    def __init__(self):
        self.__algoritm = self._get_algoritm()

    @property
    def algoritm(self) -> str:
        return self.__algoritm
    
    def _get_algoritm(self) -> str:
        algoritm = 'HS256'
        return algoritm if algoritm else None