from abc import ABC, abstractmethod

class ICreateFiscal(ABC):

    @abstractmethod
    def create(self, name:str) -> None:
        '''
        Crie um registro de fiscal

        Parâmetros:
            name: Uma string unica para o nome completo do fiscal
            
        Levanta:
            FiscalAlreadyExists: Se o fiscal ja existe
        '''