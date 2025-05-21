from pydantic import BaseModel

class CreateProjectTypeFormat(BaseModel):
    project_id:int
    types_id:int