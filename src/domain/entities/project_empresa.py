from datetime import datetime

class ProjectEmpresaEntity:

    def __init__(self, project_id:int, empresa_id:int, created_at:datetime) -> None:
        self.project_id = project_id
        self.empresa_id = empresa_id
        self.created_at = created_at