from pydantic import BaseModel

class AssociateVereadorWithAProjectFormat(BaseModel):
    cpf:str
    project_id:int