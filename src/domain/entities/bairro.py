from datetime import datetime

class BairroEntity:

    def __init__(self, bairro_id:int, name:str, created_at:datetime) -> None:
        self.bairro = bairro_id
        self.name = name
        self.created_at = created_at