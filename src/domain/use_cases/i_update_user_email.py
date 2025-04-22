from src.domain.value_objects.email import Email
from abc import ABC, abstractmethod

class IUpdateUserEmail(ABC):

    @abstractmethod
    def update(self, email:Email) -> None:
        '''
        Busca o usuario no banco de dados, e faz a alteração para o novo email no sistema:
        email ja existe: 400, EmailAlreadyExistsError
        email com formato incorreto: 400, InvalidEmailError
        '''