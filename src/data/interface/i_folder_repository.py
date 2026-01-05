from abc import ABC, abstractmethod
from src.domain.entities.folder import FolderEntity
from typing import List, Optional


class IFolderRepository(ABC):

    @abstractmethod
    def insert(self, name: str) -> None:
        """Insere uma nova pasta no banco de dados."""

    @abstractmethod
    def find_by_id(self, folder_id: int) -> FolderEntity:
        """Busca uma pasta pelo ID e retorna a entidade correspondente."""
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[FolderEntity]:
        """Busca uma pasta pelo nome e retorna a entidade correspondente ou None."""
    
    @abstractmethod
    def find_all(self) -> List[FolderEntity]:
        """Busca todas as pastas e retorna uma lista de entidades."""

    @abstractmethod
    def update(self, folder_id: int, new_name: str) -> None:
        """Atualiza o nome de uma pasta existente."""

    @abstractmethod
    def delete(self, folder_id: int) -> None:
        """Deleta uma pasta com base no ID."""
    
    @abstractmethod
    def find_all_with_pagination(self, page_size: int, page: int) -> List[FolderEntity]:
        """Busca pastas com paginação."""
    
    @abstractmethod
    def count_all(self) -> int:
        """Conta o total de pastas no sistema."""
    
    @abstractmethod
    def find_all_with_pagination_and_filter(self, page_size: int, page: int, search_term: str = None) -> List[FolderEntity]:
        """Busca pastas com paginação e filtro global."""
    
    @abstractmethod
    def count_all_with_filter(self, search_term: str = None) -> int:
        """Conta o total de pastas no sistema com filtro global."""

