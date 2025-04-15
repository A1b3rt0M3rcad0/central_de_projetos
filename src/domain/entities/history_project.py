from datetime import datetime

class HistoryProjectEntity:

    def __init__(self, 
                 history_project_id:int, 
                 project_id:int, 
                 data_name:str, 
                 description:str, 
                 updated_at:datetime) -> None:
        self.history_project_id = history_project_id
        self.project_id = project_id
        self.data_name = data_name
        self.description = description
        self.updated_at = updated_at