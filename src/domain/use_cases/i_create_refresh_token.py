from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class ICreateRefreshToken(ABC):

    @abstractmethod
    def create(self, cpf:CPF) -> None:pass