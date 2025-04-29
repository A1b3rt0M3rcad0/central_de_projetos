from abc import ABC, abstractmethod
from src.domain.entities.bairro import BairroEntity

class IBairroRepository(ABC):

    @abstractmethod
    def insert(self, name: str) -> None:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> BairroEntity:
        pass

    @abstractmethod
    def update(self, name: str, new_name: str) -> None:
        pass

    @abstractmethod
    def delete(self, name: str) -> None:
        pass
