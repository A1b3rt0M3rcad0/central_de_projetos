from src.domain.value_objects.password import Password
from abc import ABC, abstractmethod

class IUpdateUserPassword(ABC):

    @abstractmethod
    def update(self, password:Password) -> None:
        """
        Atualiza a senha de um usuário no banco de dados, criando um novo hashed password 
        e o salt correspondente para substituir a senha antiga.

        Parâmetros:
            password: A nova senha a ser atribuída ao usuário.

        Levanta:
            InvalidPasswordError (400): Caso a nova senha fornecida tenha um formato incorreto.
            InternalServerError (500): Caso ocorra um erro inesperado durante a atualização da senha.
        """