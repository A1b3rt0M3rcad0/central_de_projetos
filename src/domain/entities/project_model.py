from datetime import datetime

class ProjectFiscalEntity:

    def __init__(self, fiscal_id:int, project_id:int, created_at:datetime) -> None:
        self.fiscal_id = fiscal_id
        self.project_id = project_id
        self.created_at = created_at