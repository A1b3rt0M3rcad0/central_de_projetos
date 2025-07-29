from src.domain.entities.fiscal import FiscalEntity
from src.domain.value_objects.email import Email
from src.security.value_objects.hashed_password import HashedPassword
from abc import ABC, abstractmethod
from typing import List, Dict

class IFiscalRepository(ABC):

    @abstractmethod
    def insert(self, name:str) -> None:pass

    @abstractmethod
    def insert_all_from_user(self, name:str, email:Email, password:HashedPassword, phone:str) -> None:pass

    @abstractmethod
    def find_by_name(self, name:str) -> FiscalEntity:pass

    @abstractmethod
    def find_by_id(self, fiscal_id:int) -> FiscalEntity:pass

    @abstractmethod
    def find_all(self) -> List[FiscalEntity]:pass

    @abstractmethod
    def count_fiscals(self) -> Dict[str, int]:pass

    @abstractmethod
    def update(self, name:str, new_name:str) -> None:pass

    @abstractmethod
    def delete(self, name:str) -> None:pass