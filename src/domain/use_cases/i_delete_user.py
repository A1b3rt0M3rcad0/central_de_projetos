from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class IDeleteUser(ABC):

    @abstractmethod
    def delete(self, cpf:CPF) -> None:
        """
        Deleta um usuário do sistema com base no CPF fornecido.

        Parâmetros:
            cpf: CPF do usuário a ser deletado.

        Levanta:
            UserNotFoundError (404): Se o usuário com o CPF informado não existir.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """