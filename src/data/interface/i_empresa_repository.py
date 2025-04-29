# src/data/interface/i_empresa_repository.py
from abc import ABC, abstractmethod

class IEmpresaRepository(ABC):
    @abstractmethod
    def insert(self, name: str) -> None: pass

    @abstractmethod
    def find_by_name(self, name: str): pass

    @abstractmethod
    def update(self, name: str, new_name: str) -> None: pass

    @abstractmethod
    def delete(self, name: str) -> None: pass
