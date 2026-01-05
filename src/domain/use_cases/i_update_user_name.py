from abc import ABC, abstractmethod
from src.domain.value_objects.cpf import CPF

class IUpdateUserName(ABC):

    @abstractmethod
    def update(self, cpf:CPF, name:str) -> None:pass

