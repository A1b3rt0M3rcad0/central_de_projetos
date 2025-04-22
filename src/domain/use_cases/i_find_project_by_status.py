from src.domain.entities.project import ProjectEntity
from typing import List
from abc import ABC, abstractmethod

class IFindProjectByStatus(ABC):

    @abstractmethod
    def find(self, status_id:int) -> List[ProjectEntity]:
        '''
        Procura todos os projetos possivel pelo status_id e retorna uma lista de entidades do domain,
        caso nenhum projeto tenha sido encontrado, retorna: 400, ProjectNotFoundError
        qualquer outro error retorna 500, InternalServerError
        '''