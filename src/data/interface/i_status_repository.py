from abc import ABC, abstractmethod
from src.domain.entities.status import StatusEntity
from typing import List, Optional

class IStatusRepository(ABC):

    @abstractmethod
    def insert(self, description:str) -> None:pass

    @abstractmethod
    def find(self, status_id:Optional[int]=None, description:Optional[str]=None) -> StatusEntity:pass

    @abstractmethod
    def find_all(self) -> List[StatusEntity]:pass

    @abstractmethod
    def find_all_with_pagination(self, page_size: int, offset: int) -> List[StatusEntity]:pass

    @abstractmethod
    def count_all(self) -> int:pass

    @abstractmethod
    def update(self, status_id: int, new_description: str) -> None:pass

    @abstractmethod
    def delete(self, status_id:Optional[int]=None, description:Optional[str]=None) -> None:pass
    
    @abstractmethod
    def find_all_with_pagination_and_filter(self, page_size: int, page: int, search_term: str = None) -> List[StatusEntity]:
        """Busca status com paginação e filtro global."""
    
    @abstractmethod
    def count_all_with_filter(self, search_term: str = None) -> int:
        """Conta o total de status no sistema com filtro global."""