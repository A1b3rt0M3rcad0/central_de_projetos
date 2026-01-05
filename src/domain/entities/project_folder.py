from datetime import datetime

class ProjectFolderEntity:

    def __init__(self, id_:int, project_id:int, folder_id:int, created_at:datetime, updated_at:datetime) -> None:
        self.id = id_
        self.project_id = project_id
        self.folder_id = folder_id
        self.created_at = created_at
        self.updated_at = updated_at

