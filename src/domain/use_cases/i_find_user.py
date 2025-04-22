from src.domain.entities.user import UserEntity
from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class IFindUser(ABC):

    @abstractmethod
    def find(self, cpf:CPF) -> UserEntity:
        '''
        Procura o usuario e retorna uma entidade do domain, 
        caso n entre co usuario retorna, 404 UserNotFound,
        outros errors, retorne 500 InternalServerError
        '''