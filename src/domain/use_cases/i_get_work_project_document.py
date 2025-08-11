from abc import ABC, abstractmethod

class IGetWorkProjectDocument(ABC):
    @abstractmethod
    def get_document(self, work_project_id: int, document_name: str) -> bytes:
        """
        Obtém um documento de um work project pelo nome.
        
        Args:
            work_project_id: ID do work project
            document_name: Nome do documento
            
        Returns:
            bytes: Conteúdo do documento em bytes
            
        Raises:
            Exception: Se o documento não for encontrado
        """ 