from pydantic import BaseModel

class UpdateFiscalPasswordFormat(BaseModel):
    """
    Formato de requisição para atualizar senha do fiscal.
    
    Attributes:
        name: Nome do fiscal a ser atualizado
        password: Nova senha do fiscal
    """
    name: str
    password: str

