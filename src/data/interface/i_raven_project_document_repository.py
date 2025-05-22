from abc import ABC, abstractmethod
from typing import List
from src.domain.value_objects.document import Document
from src.infra.raven.documents.project_documents import ProjectDocuments

class IProjectDocumentRepository(ABC):
    
    @abstractmethod
    def insert_documents(self, project_id:int, project_documents:ProjectDocuments, documents:List[Document]) -> None:
        """Insert documents into a project"""
        raise NotImplementedError
    
    @abstractmethod
    def delete_document(self, project_id: int, document_name: str) -> None:
        """Delete a specific document from a project"""
        raise NotImplementedError

    @abstractmethod
    def delete_project(self, project_id:int) -> None:
        '''Deleta todo o projeto de documentos'''
        raise NotImplementedError
    
    @abstractmethod
    def get_document_names(self, project_id:int) -> List[str]:
        """Get all document names from a project"""
        raise NotImplementedError
    
    @abstractmethod
    def get_document(self, project_id:int, document_name:str, _document_class:Document) -> Document:
        """Get a specific document from a project"""
        raise NotImplementedError