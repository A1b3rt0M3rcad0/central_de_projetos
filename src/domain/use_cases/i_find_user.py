from src.domain.entities.user import UserEntity
from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class IFindUser(ABC):

    @abstractmethod
    def find(self, cpf:CPF) -> UserEntity:
        """
        Retorna o usuário com o CPF especificado.

        Parâmetros:
            cpf: CPF do usuário a ser recuperado.

        Retorno:
            Instância de UserEntity representando o usuário encontrado.

        Levanta:
            UserNotFoundError (404): Se o usuário com o CPF especificado não for encontrado.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """