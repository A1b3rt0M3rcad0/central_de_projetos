from abc import ABC, abstractmethod
from src.domain.value_objects.cpf import CPF

class IDeleteRefreshToken(ABC):

    @abstractmethod
    def delete(self, cpf:CPF) -> None:pass