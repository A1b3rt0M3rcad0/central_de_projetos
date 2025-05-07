from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime

class ProjectEntity:

    def __init__(self, 
                 project_id:int, 
                 status_id:int, 
                 verba_disponivel:MonetaryValue, 
                 andamento_do_projeto:str, 
                 start_date:datetime, 
                 expected_completion_date:datetime, 
                 end_date:datetime,
                 name:str|None=None
                 ) -> None:
        self.project_id = project_id
        self.status_id = status_id
        self.verba_disponivel = verba_disponivel
        self.andamento_do_projeto = andamento_do_projeto
        self.start_date = start_date
        self.expected_completion_date = expected_completion_date
        self.end_date = end_date
        self.name = name