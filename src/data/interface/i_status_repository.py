from abc import ABC, abstractmethod
from src.domain.entities.status import StatusEntity
from typing import List, Dict

class IStatusRepository(ABC):

    @abstractmethod
    def insert(self, description:str) -> None:pass

    @abstractmethod
    def find(self, status_id:int) -> StatusEntity:pass

    @abstractmethod
    def find_all(self) -> List[StatusEntity]:pass

    @abstractmethod
    def update(self, status_id:int, update_params:Dict) -> None:pass

    @abstractmethod
    def delete(self, status_id:int) -> None:pass