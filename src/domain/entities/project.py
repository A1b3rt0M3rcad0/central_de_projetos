from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime

class ProjectEntity:

    def __init__(self, project_id:int, status_id:int, description:str, verba_disponivel:MonetaryValue, andamento_projeto:str, data_inicio:datetime, data_final_prevista:datetime, data_finalizacao:datetime) -> None:
        self.project_id = project_id
        self.status_id = status_id
        self.description = description
        self.verba_disponivel = verba_disponivel
        self.andamento_projeto = andamento_projeto
        self.data_inicio = data_inicio
        self.data_final_prevista = data_final_prevista
        self.data_finalizacao = data_finalizacao