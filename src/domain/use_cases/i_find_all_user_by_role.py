from abc import ABC, abstractmethod
from typing import List
from src.domain.value_objects.roles import Role
from src.domain.entities.user import UserEntity

class IFindAllUserByRole(ABC):

    @abstractmethod
    def find(self, role:Role) -> List[UserEntity]:pass