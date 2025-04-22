from src.domain.entities.status import StatusEntity
from abc import ABC, abstractmethod

class IFindStatus(ABC):

    @abstractmethod
    def find(self, status_id:int) -> StatusEntity:
        """
        Retorna o status com o ID especificado.

        Parâmetros:
            status_id: ID do status a ser recuperado.

        Retorno:
            Instância de StatusEntity representando o status encontrado.

        Levanta:
            StatusNotFoundError (404): Se o status com o ID especificado não for encontrado.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """