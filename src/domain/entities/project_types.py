from datetime import datetime

class ProjectTypeEntity:

    def __init__(self, types_id:int, project_id:int, created_at:datetime) -> None:
        self.types_id = types_id
        self.project_id = project_id
        self.created_at = created_at