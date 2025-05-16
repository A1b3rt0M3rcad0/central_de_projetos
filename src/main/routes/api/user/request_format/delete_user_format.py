from pydantic import BaseModel

class DeleteUserFormat(BaseModel):
    cpf: str