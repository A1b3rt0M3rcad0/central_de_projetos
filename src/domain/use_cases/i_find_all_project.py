from abc import ABC, abstractmethod
from src.domain.entities.project import ProjectEntity
from typing import List

class IFindAllProjects(ABC):

    @abstractmethod
    def find(self) -> List[ProjectEntity]:
        '''
        Pega todos os projectos e envia eles em uma lista entidades do sistema,
        caso não encontre um projeto retornar: 404 ProjectNorFounded,
        caso aconteça qualquer outro erro, retorna 500, InternalServerError
        '''