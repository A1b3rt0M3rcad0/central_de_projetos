from pydantic import BaseModel

class LoginFormat(BaseModel):
    cpf:str
    password:str