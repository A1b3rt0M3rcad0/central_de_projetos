from abc import ABC, abstractmethod
from src.domain.entities.project import ProjectEntity
from typing import List

class IFindAllProjects(ABC):

    @abstractmethod
    def find(self) -> List[ProjectEntity]:
        """
        Retorna todos os projetos registrados no sistema.

        Retorno:
            Lista de instâncias de ProjectEntity representando todos os projetos encontrados.

        Levanta:
            ProjectNotFoundError (404): Se nenhum projeto for encontrado.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """