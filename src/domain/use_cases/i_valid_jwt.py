from abc import ABC, abstractmethod

class IValidJwt(ABC):

    @abstractmethod
    def valid(self, token:str) -> dict:
        '''valida o token e retorn um dicionario
        {
            'expired': bool,
            'invalid': bool
        }
        '''