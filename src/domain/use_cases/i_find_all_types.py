from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.types import TypesEntity

class IFindAllTypes(ABC):

    @abstractmethod
    def find(self) -> List[TypesEntity]:
        '''Retorna uma lista de entidades'''