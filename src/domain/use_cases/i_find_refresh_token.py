from src.domain.value_objects.cpf import CPF
from src.domain.entities.refresh_token import RefreshTokenEntity
from abc import ABC, abstractmethod

class IFindRefreshToken(ABC):

    @abstractmethod
    def find(self, user_cpf:CPF) -> RefreshTokenEntity:pass