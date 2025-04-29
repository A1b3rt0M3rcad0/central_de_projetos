from datetime import datetime

class EmpresaEntity:

    def __init__(self, empresa_id:int, name:str, created_at:datetime) -> None:
        self.empresa_id = empresa_id
        self.name = name
        self.created_at = created_at