from pydantic import BaseModel

class DeleteProjectFormat(BaseModel):
    project_id:int