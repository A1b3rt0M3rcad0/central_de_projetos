from pydantic import BaseModel

class DeleteProjectFolderFormat(BaseModel):
    project_id: int
    folder_id: int

