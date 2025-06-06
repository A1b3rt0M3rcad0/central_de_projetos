from src.domain.value_objects.monetary_value import MonetaryValue
from typing import List
from datetime import datetime
from src.domain.entities.bairro import BairroEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.empresa import EmpresaEntity
from src.domain.entities.types import TypesEntity
from src.domain.entities.status import StatusEntity
from src.domain.entities.history_project import HistoryProjectEntity

class ProjectEntity:

    def __init__(self, 
                 project_id:int, 
                 status_id:int, 
                 verba_disponivel:MonetaryValue, 
                 andamento_do_projeto:str, 
                 start_date:datetime, 
                 expected_completion_date:datetime, 
                 end_date:datetime,
                 name:str|None=None,
                 bairro:BairroEntity|None=None,
                 fiscal:FiscalEntity|None=None,
                 empresa:EmpresaEntity|None=None,
                 types:TypesEntity|None=None,
                 status:StatusEntity|None=None,
                 history_project:List[HistoryProjectEntity]|None=None
                 ) -> None:
        self.project_id = project_id
        self.status_id = status_id
        self.verba_disponivel = verba_disponivel
        self.andamento_do_projeto = andamento_do_projeto
        self.start_date = start_date
        self.expected_completion_date = expected_completion_date
        self.end_date = end_date
        self.name = name
        self.bairro = bairro
        self.fiscal = fiscal
        self.empresas = empresa
        self.types = types
        self.status = status
        self.history_project = history_project