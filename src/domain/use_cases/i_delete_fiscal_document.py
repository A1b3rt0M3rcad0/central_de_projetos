from abc import ABC, abstractmethod

class IDeleteFiscalDocument(ABC):

    @abstractmethod
    def delete(self, work_project_id: int, fiscal_id: int, document_name: str) -> None:
        """
        Deleta um documento específico enviado por um fiscal para um work project.

        Parâmetros:
            work_project_id: ID do work project ao qual o documento está vinculado.
            fiscal_id: ID do fiscal que enviou o documento.
            document_name: Nome do documento a ser deletado.

        Levanta:
            DocumentNotFoundError (404): Se não for encontrado um documento com o nome informado no work project.
            UnauthorizedAccessError (401): Se o fiscal não estiver autorizado a deletar o documento.
        """