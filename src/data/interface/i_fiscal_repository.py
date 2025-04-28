from src.domain.entities.fiscal import FiscalEntity
from abc import ABC, abstractmethod

class IFiscalRepository(ABC):

    @abstractmethod
    def insert(self, name:str) -> None:pass

    @abstractmethod
    def find_by_name(self, name:str) -> FiscalEntity:pass

    @abstractmethod
    def update(self, name:str, new_name:str) -> None:pass

    @abstractmethod
    def delete(self, name:str) -> None:pass