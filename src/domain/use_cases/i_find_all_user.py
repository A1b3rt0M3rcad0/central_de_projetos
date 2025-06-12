from abc import ABC, abstractmethod
from src.domain.entities.user import UserEntity
from typing import List

class IFindAllUser(ABC):

    @abstractmethod
    def find(self) -> List[UserEntity]:pass