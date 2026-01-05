#pylint:disable=W0611
from src.domain.value_objects.document import Document
from src.infra.raven.documents.project_document_fiscal import ProjectDocumentsFiscal
from abc import ABC, abstractmethod
from typing import List

class IProjectDocumentFiscalRepository(ABC):

    @abstractmethod
    def insert_fiscal_documents(self, work_project_id:int, documents:List[Document]) -> None:
        """
        Insere documentos para um work project.
        
        Args:
            work_project_id: ID do work project
            documents: Lista de documentos a serem inseridos
            
        Raises:
            Exception: Se houver erro na inserção
        """

    @abstractmethod
    def get_fiscal_document(self, work_project_id:int, fiscal_id:int, document_name:str) -> Document:
        """
        Obtém um documento específico enviado por um fiscal.
        
        Args:
            work_project_id: ID do work project
            fiscal_id: ID do fiscal
            document_name: Nome do documento
            
        Returns:
            Document: Documento encontrado
            
        Raises:
            Exception: Se o documento não for encontrado
        """


    @abstractmethod
    def get_fiscal_document_names(self, work_project_id:int, fiscal_id:int) -> List[str]:
        """
        Lista todos os nomes dos documentos enviados por um fiscal para um work project.
        
        Args:
            work_project_id: ID do work project
            fiscal_id: ID do fiscal
            
        Returns:
            List[str]: Lista com os nomes dos documentos
        """

    @abstractmethod
    def delete_fiscal_document(self, work_project_id:int, fiscal_id:int, document_name:str) -> None:
        """
        Deleta um documento específico enviado por um fiscal.
        
        Args:
            work_project_id: ID do work project
            fiscal_id: ID do fiscal
            document_name: Nome do documento a ser deletado
            
        Raises:
            Exception: Se houver erro na deleção
        """

    @abstractmethod
    def delete_all_fiscal_documents_from_work_project(self, work_project_id:int, fiscal_id:int) -> None:
        """
        Deleta todos os documentos enviados por um fiscal para um work project.
        
        Args:
            work_project_id: ID do work project
            fiscal_id: ID do fiscal
            
        Raises:
            Exception: Se houver erro na deleção
        """
    
    @abstractmethod
    def delete_all_fiscal_documents_from_fiscal(self, fiscal_id:int, work_project_ids:List[int]) -> None:
        """
        Deleta todos os documentos de todos os work projects de um fiscal.
        
        Args:
            fiscal_id: ID do fiscal
            work_project_ids: Lista de IDs dos work projects do fiscal
            
        Raises:
            Exception: Se houver erro na deleção
        """

    @abstractmethod
    def get_document_by_work_project_and_name(self, work_project_id:int, document_name:str) -> bytes:
        """
        Obtém um documento pelo work_project_id e nome do documento.
        
        Args:
            work_project_id: ID do work project
            document_name: Nome do documento
            
        Returns:
            bytes: Conteúdo do documento em bytes
            
        Raises:
            Exception: Se o documento não for encontrado
        """