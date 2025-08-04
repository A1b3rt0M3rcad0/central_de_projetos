from abc import ABC, abstractmethod

class IDeleteAllFiscalDocumentsFromProject(ABC):

    @abstractmethod
    def delete_all(self, work_project_id:int, fiscal_id:int) -> None:
        """
        Deleta todos os documentos enviados por um fiscal para um work project.

        Args:
            work_project_id: ID do work project
            fiscal_id: ID do fiscal

        Raises:
            FiscalNotFoundError (404): Se o fiscal não for encontrado
            WorkProjectNotFoundError (404): Se o work project não for encontrado
            FiscalDocumentDeleteError (500): Para qualquer outro erro durante a operação
        """