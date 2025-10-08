from abc import ABC, abstractmethod
from src.domain.value_objects.email import Email

class IUpdateFiscalEmail(ABC):

    @abstractmethod
    def update(self, name: str, email: Email) -> None:
        '''
        Atualiza o email de um fiscal

        Parâmetros:
            name: Nome do fiscal a ser atualizado
            email: Novo email do fiscal
            
        Levanta:
            FiscalNotFound: Se o fiscal não existe
            InvalidEmail: Se o email for inválido
        '''
        pass

