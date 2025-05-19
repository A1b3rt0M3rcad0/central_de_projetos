from pydantic import BaseModel

class UpdateEmpresasFormat(BaseModel):
    name:str
    new_name:str