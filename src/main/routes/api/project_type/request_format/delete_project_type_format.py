from pydantic import BaseModel

class DeleteProjectTypeFormat(BaseModel):
    project_id:int
    types_id:int