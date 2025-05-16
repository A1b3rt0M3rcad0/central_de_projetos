from pydantic import BaseModel

class CreateUserFormat(BaseModel):
    cpf: str
    email: str
    role: str
    password:str