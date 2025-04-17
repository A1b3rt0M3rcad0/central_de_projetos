from src.domain.value_objects.cpf import CPF
from datetime import datetime

class UserProjectEntity:

    def __init__(self, cpf:CPF, project_id:int, data_atribuicao:datetime) -> None:
        self.cpf = cpf
        self.project_id = project_id
        self.data_atriuicao = data_atribuicao