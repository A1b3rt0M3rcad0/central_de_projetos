from src.domain.value_objects.document import Document
from abc import ABC, abstractmethod

class IGetFiscalDocument(ABC):

    @abstractmethod
    def get(self, project_id:int, fiscal_id:int, document_name:str) -> Document:
        """
        Obtém um documento específico enviado por um fiscal para um projeto.

        Args:
            project_id: ID do projeto
            fiscal_id: ID do fiscal
            document_name: Nome do documento a ser recuperado

        Returns:
            Document: Documento encontrado

        Raises:
            FiscalDocumentNotFoundError (404): Se o documento não for encontrado
            FiscalNotFoundError (404): Se o fiscal não for encontrado
            ProjectNotFoundError (404): Se o projeto não for encontrado
            InternalServerError (500): Para qualquer outro erro durante a operação
        """