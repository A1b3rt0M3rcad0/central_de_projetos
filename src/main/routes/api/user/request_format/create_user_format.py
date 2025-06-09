from pydantic import BaseModel

class CreateUserFormat(BaseModel):
    name:str
    cpf: str
    email: str
    role: str
    password:str