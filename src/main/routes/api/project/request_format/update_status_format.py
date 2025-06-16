from pydantic import BaseModel

class UpdateStartStatusFormat(BaseModel):
    project_id:int
    status_id:int