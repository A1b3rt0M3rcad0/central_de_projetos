from pydantic import BaseModel

class LoginFiscalResponse(BaseModel):
    """
    Formato de resposta para login do fiscal via mobile.
    
    Attributes:
        token: JWT token de acesso
        message: Mensagem de sucesso
    """
    token: str
    message: str = "Login realizado com sucesso" 