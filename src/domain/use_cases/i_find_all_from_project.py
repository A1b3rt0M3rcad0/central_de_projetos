from src.domain.entities.project import ProjectEntity
from abc import ABC, abstractmethod

class IFindAllFromProject(ABC):

    @abstractmethod
    def find(self, project_id:int) -> ProjectEntity:
        '''Coleta todas as informações possiveis relacionadads ao project e devolve em uma entidade'''