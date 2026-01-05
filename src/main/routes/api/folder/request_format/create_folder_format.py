from pydantic import BaseModel

class CreateFolderFormat(BaseModel):
    name: str

