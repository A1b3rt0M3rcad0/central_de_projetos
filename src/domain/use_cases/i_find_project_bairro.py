from abc import ABC, abstractmethod
from src.domain.entities.project_bairro import ProjectBairroEntity

class IFindProjectBairro(ABC):

    @abstractmethod
    def find(self, project_id:int, bairro_id:int) -> ProjectBairroEntity:
        '''
        Procura a associação bairro projeto e retorna ela

        Parâmetros:
            project_id; ID do projeto
            bairro_id: ID do bairro
        Levanta:
            ProjectsFromBairroDoesNotExists; Caso não encontre a associação
        '''