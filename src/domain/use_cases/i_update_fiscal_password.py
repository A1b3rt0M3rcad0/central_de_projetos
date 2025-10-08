from abc import ABC, abstractmethod
from src.security.value_objects.hashed_password import HashedPassword

class IUpdateFiscalPassword(ABC):

    @abstractmethod
    def update(self, name: str, password: HashedPassword) -> None:
        '''
        Atualiza a senha de um fiscal

        Parâmetros:
            name: Nome do fiscal a ser atualizado
            password: Nova senha hasheada do fiscal
            
        Levanta:
            FiscalNotFound: Se o fiscal não existe
        '''
        pass

