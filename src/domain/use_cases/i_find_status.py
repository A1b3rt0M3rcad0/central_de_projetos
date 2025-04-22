from src.domain.entities.status import StatusEntity
from abc import ABC, abstractmethod

class IFindStatus(ABC):

    @abstractmethod
    def find(self, status_id:int) -> StatusEntity:
        '''
        Encontra o status e retorna em um entidade do domain
        caso não encontreo status retorn 404, StatusNotFoundError,
        qualquer outro erro retorne 500, InternalServerError
        '''