from src.domain.value_objects.document import Document
from abc import ABC, abstractmethod

class IGetFiscalDocument(ABC):

    @abstractmethod
    def get(self, work_project_id:int, fiscal_id:int, document_name:str) -> Document:
        """
        Obtém um documento específico enviado por um fiscal para um work project.

        Args:
            work_project_id: ID do work project
            fiscal_id: ID do fiscal
            document_name: Nome do documento a ser recuperado

        Returns:
            Document: Documento encontrado

        Raises:
            FiscalDocumentNotFoundError (404): Se o documento não for encontrado
            FiscalNotFoundError (404): Se o fiscal não for encontrado
            WorkProjectNotFoundError (404): Se o work project não for encontrado
            InternalServerError (500): Para qualquer outro erro durante a operação
        """