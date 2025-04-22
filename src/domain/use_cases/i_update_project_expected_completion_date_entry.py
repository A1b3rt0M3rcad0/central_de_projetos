from abc import ABC, abstractmethod
from datetime import datetime

class IUpdateProjectExpectedCompletionDate(ABC):

    @abstractmethod
    def update(self, project_id:int, expected_completion_date:datetime) -> None:
        '''
        Faz o updade do expected completion date, procurando ele pelo id,
        caso nao consiga fazer o update do projeto retorne 500, InternalServerError,
        se o expected_completion_date for menor que o start date, retorne 400 InvalidExpectedCompletionDateError
        '''