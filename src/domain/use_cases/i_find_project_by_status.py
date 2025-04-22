from src.domain.entities.project import ProjectEntity
from typing import List
from abc import ABC, abstractmethod

class IFindProjectByStatus(ABC):

    @abstractmethod
    def find(self, status_id:int) -> List[ProjectEntity]:
        """
        Retorna todos os projetos com o status especificado pelo status_id.

        Parâmetros:
            status_id: ID do status dos projetos a serem recuperados.

        Retorno:
            Lista de instâncias de ProjectEntity representando os projetos com o status correspondente.

        Levanta:
            ProjectNotFoundError (404): Se nenhum projeto com o status especificado for encontrado.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """