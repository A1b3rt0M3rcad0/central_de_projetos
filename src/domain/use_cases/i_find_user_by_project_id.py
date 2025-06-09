from abc import ABC, abstractmethod
from src.domain.entities.user import UserEntity

class IFindUserByProjectId(ABC):

    @abstractmethod
    def find(self, project_id) -> UserEntity | None:pass