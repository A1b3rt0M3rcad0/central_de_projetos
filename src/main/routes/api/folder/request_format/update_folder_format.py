from pydantic import BaseModel

class UpdateFolderFormat(BaseModel):
    folder_id: int
    new_name: str

