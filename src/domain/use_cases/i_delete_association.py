from abc import ABC, abstractmethod
from src.domain.value_objects.cpf import CPF

class IDeleteAssociation(ABC):

    @abstractmethod
    def delete(self, cpf:CPF, project_id:int) -> None:
        """
        Deleta uma associação entre vereador e projeto

        Parâmetros:
            cpf: cpf do vereador.
            project_id: ID do projeto.

        Levanta:
            AssociationNotFoundError (404): Se não encontrar a associação para se deletar
            InternalServerError (500): Se ocorrer qualquer erro durante a criação do status.
        """