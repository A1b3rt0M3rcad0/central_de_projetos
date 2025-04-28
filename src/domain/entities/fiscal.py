from datetime import datetime

class FiscalEntity:

    def __init__(self, fiscal_id:int, name:str, created_at:datetime) -> None:
        self.fiscal_id = fiscal_id
        self.name = name
        self.created_at = created_at
