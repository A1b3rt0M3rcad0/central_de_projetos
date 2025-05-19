from pydantic import BaseModel

class UpdateProjectNameFormat(BaseModel):
    project_id:int
    name:str