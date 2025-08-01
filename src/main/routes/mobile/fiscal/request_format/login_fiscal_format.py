from pydantic import BaseModel, EmailStr

class LoginFiscalFormat(BaseModel):
    """
    Formato de requisição para login do fiscal via mobile.
    
    Attributes:
        email: Email do fiscal
        password: Senha do fiscal
    """
    email: EmailStr
    password: str 