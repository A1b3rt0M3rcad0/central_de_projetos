from abc import ABC, abstractmethod

class IUpdateProjectAndamento(ABC):

    @abstractmethod
    def update(self, project_id:int, andamento_do_projeto:str) -> None:
        '''
        Faz o updade do andamento do projeto, procurando ele pelo id,
        caso nao consiga fazer o update do projeto retorne 500, InternalServerError
        '''