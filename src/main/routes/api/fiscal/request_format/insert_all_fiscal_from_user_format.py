from pydantic import BaseModel, EmailStr

class InsertAllFiscalFromUserFormat(BaseModel):
    """
    Formato de requisição para inserir fiscal com todos os dados.
    
    Attributes:
        name: Nome completo do fiscal
        email: Email do fiscal
        password: Senha do fiscal
        phone: Telefone do fiscal
    """
    name: str
    email: EmailStr
    password: str
    phone: str 