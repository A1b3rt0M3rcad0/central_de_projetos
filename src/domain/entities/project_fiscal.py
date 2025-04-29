from datetime import datetime

class ProjectFiscalEntity:

    def __init__(self, project_id:int, fiscal_id:int, created_at:datetime) -> None:
        self.project_id = project_id
        self.fiscal_id = fiscal_id
        self.created_at = created_at