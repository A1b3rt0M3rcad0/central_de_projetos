from abc import ABC, abstractmethod

class ICreateStatus(ABC):

    @abstractmethod
    def create(self, description:str) -> None:
        '''
        Cria o status e insere no banco de dados, caso o status n seja criado
        retorne um erro 500, InternalServerError
        '''