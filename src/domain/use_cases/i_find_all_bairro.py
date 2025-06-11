from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.bairro import BairroEntity

class IFindAllBairro(ABC):

    @abstractmethod
    def find(self) -> List[BairroEntity]:pass