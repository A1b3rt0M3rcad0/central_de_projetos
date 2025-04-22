from src.domain.value_objects.password import Password
from abc import ABC, abstractmethod

class IUpdateUserPassword(ABC):

    @abstractmethod
    def update(self, password:Password) -> None:
        '''
        Busca o usuario no banco de dados, e faz a alteração para o novo password no sistema, criando um novo hashedpassword, juntamente com seu salt
        para ser salvo no lugar dos antigos
        password com formato incorreto: 400, InvalidPasswordError
        '''