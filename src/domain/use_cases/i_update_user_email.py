from src.domain.value_objects.email import Email
from abc import ABC, abstractmethod

class IUpdateUserEmail(ABC):

    @abstractmethod
    def update(self, email:Email) -> None:
        """
        Atualiza o e-mail de um usuário no banco de dados.

        Parâmetros:
            email: O novo e-mail a ser atribuído ao usuário.

        Levanta:
            EmailAlreadyExistsError (400): Caso o e-mail fornecido já exista no sistema.
            InvalidEmailError (400): Caso o e-mail fornecido tenha um formato incorreto.
            InternalServerError (500): Caso ocorra um erro inesperado durante a atualização do e-mail.
        """