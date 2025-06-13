from abc import ABC, abstractmethod
from src.domain.value_objects.cpf import CPF
from src.security.value_objects.hashed_password import HashedPassword
from src.security.cryptography.interface.i_salt import ISalt
from src.domain.value_objects.roles import Role
from src.domain.value_objects.email import Email
from src.domain.entities.user import UserEntity
from typing import Dict, Optional, List

class IUserRepository(ABC):

    @abstractmethod
    def insert(self, cpf:CPF, password:HashedPassword, salt:ISalt, role: Role, email:Email) -> None:pass

    @abstractmethod
    def find(self, cpf:CPF) -> UserEntity:pass

    @abstractmethod
    def find_by_email(self, email:Email) -> Optional[UserEntity]:pass

    @abstractmethod
    def find_all(self) -> List[UserEntity]:pass

    @abstractmethod
    def find_all_by_role(self, role:Role) -> List[UserEntity]:pass

    @abstractmethod
    def update(self, cpf:CPF, update_params:Dict) -> None:pass

    @abstractmethod
    def delete(self, cpf:CPF) -> None:pass