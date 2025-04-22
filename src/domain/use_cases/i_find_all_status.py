from src.domain.entities.status import StatusEntity
from typing import List
from abc import ABC, abstractmethod

class IFindAllStatus(ABC):

    @abstractmethod
    def find(self) -> List[StatusEntity]:
        '''
        Encontra todos os status e retorna em uma lista de entidades do domain
        caso não encontre um status retorna 404, StatusNotFoundError,
        qualquer outro erro retorne 500, InternalServerError
        '''