from abc import ABC, abstractmethod
from src.domain.entities.fiscal import FiscalEntity

class IFindFiscalByName(ABC):

    @abstractmethod
    def find(self, name:str) -> FiscalEntity:
        '''
        Realiza a busca de um fiscal pelo nome e retorna uma entidade fiscal

        Parãmetros:
            name: str do nome do fiscal
        Levanta:
            FiscalDoesNotExists: caso não encontre nenhum fiscal com esse nome
        '''