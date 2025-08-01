from abc import ABC, abstractmethod

class IDeleteAllFiscalDocumentsFromProject(ABC):

    @abstractmethod
    def delete_all(self, project_id:int, fiscal_id:int) -> None:
        """
        Deleta todos os documentos enviados por um fiscal para um projeto.

        Args:
            project_id: ID do projeto
            fiscal_id: ID do fiscal

        Raises:
            FiscalNotFoundError (404): Se o fiscal não for encontrado
            ProjectNotFoundError (404): Se o projeto não for encontrado
            FiscalDocumentDeleteError (500): Para qualquer outro erro durante a operação
        """