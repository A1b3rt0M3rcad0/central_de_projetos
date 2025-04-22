from abc import ABC, abstractmethod
from datetime import datetime

class IUpdateProjectStartDate(ABC):

    @abstractmethod
    def update(self, project_id:int, start_date:datetime) -> None:
        '''
        Faz o updade do start date, procurando ele pelo id,
        caso nao consiga fazer o update do projeto retorne 500, InternalServerError
        '''