from pydantic import BaseModel

class UpdateUserPasswordFormat(BaseModel):
    cpf:str
    password:str