from datetime import datetime

class FolderEntity:

    def __init__(self, folder_id:int, name:str, created_at:datetime, updated_at:datetime) -> None:
        self.folder_id = folder_id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

