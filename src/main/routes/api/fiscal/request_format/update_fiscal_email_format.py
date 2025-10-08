from pydantic import BaseModel, EmailStr

class UpdateFiscalEmailFormat(BaseModel):
    """
    Formato de requisição para atualizar email do fiscal.
    
    Attributes:
        name: Nome do fiscal a ser atualizado
        email: Novo email do fiscal
    """
    name: str
    email: EmailStr

