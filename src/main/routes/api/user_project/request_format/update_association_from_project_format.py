from pydantic import BaseModel

class UpdateAssociationFromProjectFormat(BaseModel):
    cpf:str
    new_cpf:str
    project_id:int