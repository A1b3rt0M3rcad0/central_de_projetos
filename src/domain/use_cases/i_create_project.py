from abc import ABC, abstractmethod
from datetime import datetime
from src.domain.value_objects.monetary_value import MonetaryValue
from typing import Optional

class ICreateProject(ABC):

    @abstractmethod
    def create(self, 
               status_id:int, 
               verba_disponivel:Optional[MonetaryValue]=None, 
               andamento_do_projeto:Optional[str]=None, 
               start_date:Optional[datetime]=None, 
               expected_completion_date:Optional[datetime]=None, 
               end_date:Optional[datetime]=None
               ) -> None:
        '''
        Cria um Projeto novo no banco de dados, sendo necessário apenas o id do status do projeto,
        caso não consiga criar retorne um error: 500, CreateProjectError
        '''