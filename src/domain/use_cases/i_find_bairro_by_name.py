from abc import ABC, abstractmethod
from src.domain.entities.bairro import BairroEntity

class IFindBairroByName(ABC):

    @abstractmethod
    def find(self, name:str) -> BairroEntity:
        '''
        Procura o bairro pelo nome exato

        Parâmetros:
            name: nome do bairro exato que deseja procurar
        Levanta:
            BairroNotExists: caso o bairro não tenha sido encontrado
        '''