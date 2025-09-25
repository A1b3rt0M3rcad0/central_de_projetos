from abc import ABC, abstractmethod
from src.domain.entities.empresa import EmpresaEntity
from typing import List, Dict

class IEmpresaRepository(ABC):
    @abstractmethod
    def insert(self, name: str) -> None: pass

    @abstractmethod
    def find_by_name(self, name: str) -> EmpresaEntity: pass

    @abstractmethod
    def find_all(self) -> List[EmpresaEntity]:pass

    @abstractmethod
    def count_empresas(self) -> Dict[str, int]:pass

    @abstractmethod
    def get_count_projects_by_empresas(self) -> Dict[str, int]:pass

    @abstractmethod
    def update(self, name: str, new_name: str) -> None: pass

    @abstractmethod
    def delete(self, name: str) -> None: pass
    
    @abstractmethod
    def find_all_with_pagination(self, page_size: int, page: int) -> List[EmpresaEntity]:
        """Busca empresas com paginação."""
    
    @abstractmethod
    def count_all(self) -> int:
        """Conta o total de empresas no sistema."""