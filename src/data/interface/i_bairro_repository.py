from abc import ABC, abstractmethod
from src.domain.entities.bairro import BairroEntity
from typing import List

class IBairroRepository(ABC):

    @abstractmethod
    def insert(self, name: str) -> None:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> BairroEntity:
        pass

    @abstractmethod
    def find_by_id(self, bairro_id: int) -> BairroEntity:
        pass

    @abstractmethod
    def find_all(self) -> List[BairroEntity]:pass

    @abstractmethod
    def update(self, name: str, new_name: str) -> None:
        pass

    @abstractmethod
    def delete(self, name: str) -> None:
        pass
