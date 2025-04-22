from abc import ABC, abstractmethod

class IDeleteStatus(ABC):

    @abstractmethod
    def delete(self, status_id:int) -> None:
        '''
        Deleta o status,
        Caso o status nao exista para deletar, retorne 404, StatusNotFoundError,
        outro erro retorne 500 InternalServerError
        '''