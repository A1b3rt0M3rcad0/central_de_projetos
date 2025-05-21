from pydantic import BaseModel

class DeleteAssociationFormat(BaseModel):
    cpf:str
    project_id:int