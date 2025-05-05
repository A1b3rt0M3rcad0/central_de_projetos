from abc import ABC, abstractmethod
from src.domain.entities.fiscal import FiscalEntity

class IFindFiscalById(ABC):

    @abstractmethod
    def find(self, fiscal_id:str) -> FiscalEntity:
        '''
        Procura o fiscal pelo id

        Parâmetros:
            fiscal_id: id do fiscal que deseja procurar
        Levanta:
            FiscalNotExists: caso o fiscal não tenha sido encontrado
        '''