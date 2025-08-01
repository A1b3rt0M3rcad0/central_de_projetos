from abc import ABC, abstractmethod

class IDeleteFiscalDocument(ABC):

    @abstractmethod
    def delete(self, project_id:int, fiscal_id:int, document_name:str) -> None:
        """
        Deleta um documento específico enviado por um fiscal para um projeto.

        Args:
            project_id: ID do projeto
            fiscal_id: ID do fiscal
            document_name: Nome do documento a ser deletado

        Raises:
            FiscalDocumentNotFoundError (404): Se o documento não for encontrado
            FiscalNotFoundError (404): Se o fiscal não for encontrado
            ProjectNotFoundError (404): Se o projeto não for encontrado
            FiscalDocumentDeleteError (500): Para qualquer outro erro durante a operação
        """