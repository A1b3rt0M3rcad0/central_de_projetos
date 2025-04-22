from abc import ABC, abstractmethod
from src.domain.entities.history_project import HistoryProjectEntity
from typing import List

class IFindAllHistoryFromProject(ABC):

    @abstractmethod
    def find(self, project_id:int) -> List[HistoryProjectEntity]:
        """
        Retorna todo o histórico de modificações de um projeto.

        Parâmetros:
            project_id: ID do projeto para o qual o histórico de modificações será recuperado.

        Retorno:
            Lista de instâncias de HistoryProjectEntity representando as modificações do projeto.

        Levanta:
            ProjectNotFoundError (404): Se o projeto com o ID informado não for encontrado.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """