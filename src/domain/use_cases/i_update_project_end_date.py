from abc import ABC, abstractmethod
from datetime import datetime

class IUpdateProjectEndDate(ABC):

    @abstractmethod
    def update(self, project_id:int, end_date:datetime) -> None:
        '''
        Faz o updade do end_date, procurando ele pelo id,
        caso nao consiga fazer o update do projeto retorne 500, InternalServerError,
        se a data de termino for menor que a data de inicio retorne um erro, 400, InvalidEndDateError
        '''