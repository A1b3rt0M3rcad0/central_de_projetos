from pydantic import BaseModel

class DeleteProjectBairroFormat(BaseModel):
    project_id:int
    bairro_id:int