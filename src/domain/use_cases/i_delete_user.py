from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class IDeleteUser(ABC):

    @abstractmethod
    def delete(self, cpf:CPF) -> None:
        '''
        Deleta o usuario do sistema, caso o usuario n exista
        retorna 404, UserNotFound,
        qualquer outro erro retorna 500, InternalServerError
        '''