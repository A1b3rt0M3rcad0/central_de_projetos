from pydantic import BaseModel

class UpdateUserEmailFormat(BaseModel):
    cpf:str
    email:str