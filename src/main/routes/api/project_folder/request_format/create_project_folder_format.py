from pydantic import BaseModel

class CreateProjectFolderFormat(BaseModel):
    project_id: int
    folder_id: int

