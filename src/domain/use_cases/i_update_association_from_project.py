from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class IUpdateAssociationFromProject(ABC):

    @abstractmethod
    def update(self, cpf:CPF, project_id:int, new_cpf:CPF) -> None:
        """
        Substitui o vereador associado a um projeto por outro.

        Parâmetros:
            cpf: CPF atual do vereador associado.
            project_id: ID do projeto.
            new_cpf: Novo CPF a ser associado ao projeto.

        Levanta:
            InvalidRoleError (400): Se o novo CPF não pertence a um usuário com a role 'vereador'.
            UserNotFoundError (404): Se o novo CPF não estiver cadastrado no sistema.
            AssociationNotFoundError (404): Se não existir associação entre o projeto e o CPF atual.
            InternalServerError (500): Para erros inesperados.
        """