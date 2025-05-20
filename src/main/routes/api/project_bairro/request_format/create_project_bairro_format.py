from pydantic import BaseModel

class CreateProjectBairroFormat(BaseModel):
    project_id:int
    bairro_id:int