from abc import ABC, abstractmethod
from src.domain.entities.bairro import BairroEntity
from typing import List, Dict

class IBairroRepository(ABC):

    @abstractmethod
    def insert(self, name: str) -> None:pass

    @abstractmethod
    def find_by_name(self, name: str) -> BairroEntity:pass

    @abstractmethod
    def find_by_id(self, bairro_id: int) -> BairroEntity:pass

    @abstractmethod
    def find_all(self) -> List[BairroEntity]:pass

    @abstractmethod
    def count_bairros(self) -> Dict[str, int]:pass

    @abstractmethod
    def update(self, name: str, new_name: str) -> None:pass

    @abstractmethod
    def delete(self, name: str) -> None:pass
    
    @abstractmethod
    def find_all_with_pagination(self, page_size: int, page: int) -> List[BairroEntity]:
        """Busca bairros com paginação."""
    
    @abstractmethod
    def count_all(self) -> int:
        """Conta o total de bairros no sistema."""
    
    @abstractmethod
    def find_all_with_pagination_and_filter(self, page_size: int, page: int, search_term: str = None) -> List[BairroEntity]:
        """Busca bairros com paginação e filtro global."""
    
    @abstractmethod
    def count_all_with_filter(self, search_term: str = None) -> int:
        """Conta o total de bairros no sistema com filtro global."""