from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class IUpdateUserCPF(ABC):

    @abstractmethod
    def update(self, cpf:CPF) -> None:
        '''
        Busca o usuario no banco de dados, e faz a alteração para o novo cpf no sistema:
        cpf ja existe: 400, CpfAlreadyExistsError
        cpf com formato incorreto: 400 InvalidCpfError
        '''