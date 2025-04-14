from abc import ABC, abstractmethod
from src.domain.value_objects.cpf import CPF
from src.domain.entities.user_project import UserProjectEntity
from typing import List, Dict, Optional

class IUserProject(ABC):

    @abstractmethod
    def insert(self, cpf_user:CPF, project_id:int) -> None:pass

    @abstractmethod
    def find(self, cpf_user:CPF, project_id:int) -> UserProjectEntity:pass

    @abstractmethod
    def find_all(self) -> List[Optional[UserProjectEntity]]:pass

    @abstractmethod
    def update(self, cpf_user:CPF, project_id:int, update_params:Dict) -> None:pass

    @abstractmethod
    def delete(self, cpf_user:CPF, project_id:int) -> None:pass