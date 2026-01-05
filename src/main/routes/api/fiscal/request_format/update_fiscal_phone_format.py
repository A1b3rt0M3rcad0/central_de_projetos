from pydantic import BaseModel

class UpdateFiscalPhoneFormat(BaseModel):
    """
    Formato de requisição para atualizar telefone do fiscal.
    
    Attributes:
        name: Nome do fiscal a ser atualizado
        phone: Novo telefone do fiscal
    """
    name: str
    phone: str

