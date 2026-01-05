from pydantic import BaseModel
from typing import Optional

class UpdateUserPersonalDataFormat(BaseModel):
    cpf: str
    name: Optional[str] = None
    email: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None

