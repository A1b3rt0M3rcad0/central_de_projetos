from abc import ABC, abstractmethod

class IDeleteStatus(ABC):

    @abstractmethod
    def delete(self, status_id:int) -> None:
        """
        Deleta um status do banco de dados com base no ID fornecido.

        Parâmetros:
            status_id: ID do status a ser deletado.

        Levanta:
            StatusNotFoundError (404): Se o status informado não existir.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """