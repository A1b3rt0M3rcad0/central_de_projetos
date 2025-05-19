from pydantic import BaseModel

class UpdateProjectAndamentoFormat(BaseModel):
    project_id:int
    andamento_do_projeto:str