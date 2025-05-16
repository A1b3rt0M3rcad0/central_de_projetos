from pydantic import BaseModel

class FindUserFormat(BaseModel):
    user_cpf:str