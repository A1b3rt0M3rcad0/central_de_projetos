from abc import ABC, abstractmethod
from typing import List, Dict
from src.infra.mongo.models.project_document_model import ProjectDocumentModel

class IProjectDocumentRepository(ABC):

    @abstractmethod
    def create_project_document(self, project_model: ProjectDocumentModel) -> None:
        """Cria um documento de projeto no banco de dados."""

    @abstractmethod
    def find_project_document(self, project_id: int) -> List[Dict[str, bytes]]:
        """Busca documentos relacionados a um projeto pelo ID."""

    @abstractmethod
    def insert_documents_into_project(self, project_model: ProjectDocumentModel) -> None:
        """Insere documentos adicionais em um projeto existente."""

    @abstractmethod
    def delete_document_from_project(self, project_id: int, document_name: str) -> None:
        """Remove um documento específico de um projeto, baseado no nome."""

    @abstractmethod
    def delete_all_documents_from_project(self, project_id: int) -> None:
        """Remove todos os documentos de um projeto."""