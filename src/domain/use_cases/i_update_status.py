from abc import ABC, abstractmethod

class IUpdateStatusDescription(ABC):

    @abstractmethod
    def update(self, description:str) -> None:
        '''
        Realiza o update do description do status,
        caso a description ja exista, retorna 400, StatusDescriptionError
        outro erro retorna, 500 InternalServerError
        '''