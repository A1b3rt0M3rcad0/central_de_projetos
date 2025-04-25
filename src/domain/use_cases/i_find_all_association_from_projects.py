from typing import List
from src.domain.entities.user_project import UserProjectEntity
from abc import ABC, abstractmethod

class IFindAllAssociationfromProjects(ABC):

    @abstractmethod
    def find(self) -> List[UserProjectEntity]:
        """
        Retorna uma lista de todas as associações entre usuários e projetos.

        Retorno:
            Lista de instâncias de UserProjectEntity representando as associações encontradas.

        Levanta:
            AssociationNotFoundError (404): Se nenhuma associação for encontrada.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """