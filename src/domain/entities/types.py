from datetime import datetime

class TypesEntity:

    def __init__(self, types_id:int, name:str, created_at:datetime) -> None:
        self.types_id = types_id
        self.name = name
        self.created_at = created_at