from pydantic import BaseModel

class DeleteFolderFormat(BaseModel):
    folder_id: int

