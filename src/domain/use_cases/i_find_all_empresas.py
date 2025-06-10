from abc import ABC, abstractmethod
from src.domain.entities.empresa import EmpresaEntity
from typing import List

class IFindAllEmpresas(ABC):

    @abstractmethod
    def find(self) -> List[EmpresaEntity]:pass