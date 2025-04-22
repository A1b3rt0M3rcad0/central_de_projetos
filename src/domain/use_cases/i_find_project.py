from src.domain.entities.project import ProjectEntity
from abc import ABC, abstractmethod

class IFindProject(ABC):

    @abstractmethod
    def find(self, project_id:int) -> ProjectEntity:
        """
        Retorna o projeto com o ID especificado.

        Parâmetros:
            project_id: ID do projeto a ser recuperado.

        Retorno:
            Instância de ProjectEntity representando o projeto encontrado.

        Levanta:
            ProjectNotFoundError (404): Se o projeto com o ID especificado não for encontrado.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """