from datetime import datetime

class ProjectBairroEntity:

    def __init__(self, project_id:int, bairro_id:int, created_at:datetime) -> None:
        self.project_id = project_id
        self.bairro_id = bairro_id
        self.created_at = created_at