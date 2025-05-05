from abc import ABC, abstractmethod
from src.domain.entities.types import TypesEntity

class IFindTypeByExactName(ABC):
    
    @abstractmethod
    def find(self, name:str) -> TypesEntity:
        '''
        Procura um tipo pelo seu nome exato

        Parâmetros:
            name: Nome do typo que procura
        Levanta:
            TypesNotExists: Caso não encotre nenhum type
        '''