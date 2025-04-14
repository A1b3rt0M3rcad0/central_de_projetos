from datetime import datetime

class StatusEntity:

    def __init__(self, status_id:int, description:str, created_at:datetime) -> None:
        self.status_id = status_id
        self.description = description
        self.created_at = created_at
        