from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class IUpdateRefreshToken(ABC):

    @abstractmethod
    def update(self, user_cpf:CPF, new_token:str) -> None:pass