from typing import List
from src.domain.entities.fiscal import FiscalEntity
from abc import ABC, abstractmethod

class IFindAllFiscal(ABC):

    @abstractmethod
    def find(self) -> List[FiscalEntity]:pass