from src.domain.entities.refresh_token import RefreshTokenEntity
from abc import ABC, abstractmethod
from src.domain.value_objects.cpf import CPF

class IRefreshTokenRepository(ABC):

    @abstractmethod
    def insert(self, user_cpf:CPF, token:str) -> None:pass

    @abstractmethod
    def find(self, user_cpf:CPF) -> RefreshTokenEntity:pass

    @abstractmethod
    def update(self, user_cpf:CPF, new_token:str) -> None:pass

    @abstractmethod
    def delete(self, user_cpf:CPF) -> None:pass