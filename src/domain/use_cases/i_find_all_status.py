from src.domain.entities.status import StatusEntity
from typing import List
from abc import ABC, abstractmethod

class IFindAllStatus(ABC):

    @abstractmethod
    def find(self) -> List[StatusEntity]:
        """
        Retorna todos os status registrados no sistema.

        Retorno:
            Lista de instâncias de StatusEntity representando todos os status encontrados.

        Levanta:
            StatusNotFoundError (404): Se nenhum status for encontrado.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """