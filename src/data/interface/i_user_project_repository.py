from abc import ABC, abstractmethod
from src.domain.value_objects.cpf import CPF
from src.domain.entities.user_project import UserProjectEntity
from src.domain.entities.user import UserEntity
from typing import List, Dict, Optional

class IUserProjectRepository(ABC):

    @abstractmethod
    def insert(self, cpf_user:CPF, project_id:int) -> None:pass

    @abstractmethod
    def find(self, cpf_user:CPF, project_id:int) -> UserProjectEntity:pass

    @abstractmethod
    def find_all_from_cpf(self, cpf_user:CPF) -> List[UserProjectEntity]:pass

    @abstractmethod
    def find_all(self) -> List[Optional[UserProjectEntity]]:pass

    @abstractmethod
    def find_user_by_project_id(self, project_id:int) -> UserEntity:pass

    @abstractmethod
    def update(self, cpf_user:CPF, project_id:int, update_params:Dict) -> None:pass

    @abstractmethod
    def delete(self, cpf_user:CPF, project_id:int) -> None:pass

    @abstractmethod
    def delete_all_from_project(self, project_id:int) -> None:pass