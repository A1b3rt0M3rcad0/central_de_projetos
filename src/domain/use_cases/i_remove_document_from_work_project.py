from abc import ABC, abstractmethod

class IRemoveDocumentFromWorkProject(ABC):

    @abstractmethod
    def remove(self, work_project_id: int, document_name: str) -> None:
        """
        Remove um documento da lista de documentos de um work project.

        Parâmetros:
            work_project_id: ID do work project.
            document_name: Nome do documento a ser removido da lista.

        Levanta:
            WorkProjectNotFoundError (404): Se o work project não for encontrado.
            DocumentNotFoundError (404): Se o documento não estiver na lista.
        """ 