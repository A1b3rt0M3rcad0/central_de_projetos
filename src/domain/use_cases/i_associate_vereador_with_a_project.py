from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class IAssociateVereadorWithAProject(ABC):

    @abstractmethod
    def associate(self, cpf_user:CPF, project_id:int) -> None:
        """
        Associa um vereador a um projeto.

        Antes de realizar a associação, valida se o usuário tem o papel de 'vereador'.

        Parâmetros:
            cpf_user: CPF do usuário a ser associado.
            project_id: ID do projeto ao qual o vereador será associado.

        Levanta:
            InvalidRoleError (400): Se o usuário não possuir o papel de vereador.
            InvalidAssociationError (400): Se a associação já existir.
            UserNotFoundError (404): Se o CPF informado não estiver cadastrado.
            ProjectNotFoundError (404): Se o projeto informado não existir.
            InternalServerError (500): Para erros inesperados.
        """