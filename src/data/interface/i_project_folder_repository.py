from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.project_folder import ProjectFolderEntity

class IProjectFolderRepository(ABC):

    @abstractmethod
    def insert(self, project_id: int, folder_id: int) -> None:
        """Insere uma associação entre projeto e pasta"""

    @abstractmethod
    def find(self, project_id: int, folder_id: int) -> ProjectFolderEntity:
        """Busca uma associação específica entre projeto e pasta"""

    @abstractmethod
    def find_all_from_folder(self, folder_id: int) -> List[ProjectFolderEntity]:
        """Busca todos os projetos associados a uma pasta"""
    
    @abstractmethod
    def find_all_from_project(self, project_id: int) -> List[ProjectFolderEntity]:
        """Busca todas as pastas associadas a um projeto"""

    @abstractmethod
    def delete(self, project_id: int, folder_id: int) -> None:
        """Remove a associação entre projeto e pasta"""
    
    @abstractmethod
    def delete_all_from_project(self, project_id: int) -> None:
        """Remove todas as associações de pastas de um projeto"""
    
    @abstractmethod
    def delete_all_from_folder(self, folder_id: int) -> None:
        """Remove todas as associações de projetos de uma pasta"""

