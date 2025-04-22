from abc import ABC, abstractmethod
from typing import Optional

class ICreateHistoryProject(ABC):

    @abstractmethod
    def create(self, project_id:int, data_name:str, description:Optional[str]=None) -> None:
        """
        Cria um registro de histórico de modificações para um projeto.

        Esse histórico é gerado a cada alteração de dados ou adição de documentos ao projeto.

        Parâmetros:
            project_id: ID do projeto que será associado ao histórico.
            data_name: Nome do dado ou evento registrado.
            description: (Opcional) Descrição adicional da modificação.

        Levanta:
            ProjectNotFoundError (404): Se o projeto informado não existir.
            InternalServerError (500): Para erros inesperados.
        """