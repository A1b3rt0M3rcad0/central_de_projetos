from src.domain.entities.fiscal import FiscalEntity
from src.domain.value_objects.email import Email
from src.security.value_objects.hashed_password import HashedPassword
from abc import ABC, abstractmethod
from typing import List, Dict

class IFiscalRepository(ABC):

    @abstractmethod
    def insert(self, name:str) -> None:pass

    @abstractmethod
    def insert_all_from_fiscal(self, name:str, email:Email, password:HashedPassword, phone:str) -> None:pass

    @abstractmethod
    def insert_refresh_token(self, fiscal_id:int, refresh_token:str) -> None:pass

    @abstractmethod
    def find_by_name(self, name:str) -> FiscalEntity:pass

    @abstractmethod
    def find_by_id(self, fiscal_id:int) -> FiscalEntity:pass

    @abstractmethod
    def find_by_email(self, email:Email) -> FiscalEntity:pass

    @abstractmethod
    def find_all(self) -> List[FiscalEntity]:pass

    @abstractmethod
    def count_fiscals(self) -> Dict[str, int]:pass

    @abstractmethod
    def update(self, name:str, new_name:str) -> None:pass

    @abstractmethod
    def update_email(self, name:str, email:Email) -> None:pass

    @abstractmethod
    def update_password(self, name:str, password:HashedPassword) -> None:pass

    @abstractmethod
    def update_phone(self, name:str, phone:str) -> None:pass

    @abstractmethod
    def delete(self, name:str) -> None:pass
    
    @abstractmethod
    def find_all_with_pagination(self, page_size: int, page: int) -> List[FiscalEntity]:
        """Busca fiscais com paginação."""
    
    @abstractmethod
    def count_all(self) -> int:
        """Conta o total de fiscais no sistema."""
    
    @abstractmethod
    def find_all_with_pagination_and_filter(self, page_size: int, page: int, search_term: str = None) -> List[FiscalEntity]:
        """Busca fiscais com paginação e filtro global."""
    
    @abstractmethod
    def count_all_with_filter(self, search_term: str = None) -> int:
        """Conta o total de fiscais no sistema com filtro global."""
    
    @abstractmethod
    def update_status(self, fiscal_id: int, is_active: int) -> None:
        """Atualiza o status (ativo/inativo) de um fiscal."""