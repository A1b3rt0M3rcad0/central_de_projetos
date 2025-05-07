from src.domain.entities.project import ProjectEntity
from abc import ABC, abstractmethod

class IFindProjectByName(ABC):

    @abstractmethod
    def find(self, name:str) -> ProjectEntity:
        '''
        Procura um projeto pelo seu nome

        Parãmetros:
            name: nome do projeto
        levanta:
            None
        '''