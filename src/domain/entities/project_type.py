from datetime import datetime

class ProjectTypeEntity:

    def __init__(self, project_id:int, type_id:int, created_at:datetime) -> None:
        self.type_id = type_id
        self.project_id = project_id
        self.created_at = created_at