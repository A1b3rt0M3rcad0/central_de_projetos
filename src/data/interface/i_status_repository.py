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
    def update(self, status_id: int, new_description: str) -> None:pass

    @abstractmethod
    def delete(self, status_id:Optional[int]=None, description:Optional[str]=None) -> None:pass