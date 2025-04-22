from src.domain.entities.project import ProjectEntity
from abc import ABC, abstractmethod

class IFindProject(ABC):

    @abstractmethod
    def find(self, project_id:int) -> ProjectEntity:
        '''
        Procura o projeto no banco de dados e retorna uma entidade do domain, 
        Caso o projeto não tenha sido encotrado retorn 404, ProjectNotFoundedError,
        qualquer outro erro retorne 500, InternalServerError
        '''