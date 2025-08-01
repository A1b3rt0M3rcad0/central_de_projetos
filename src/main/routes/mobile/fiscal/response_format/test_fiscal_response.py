from pydantic import BaseModel


class FiscalTestResponse(BaseModel):
    """
    Resposta para o endpoint de teste dos fiscais mobile.
    """
    message: str
    fiscal_email: str
    fiscal_role: str
    timestamp: str
    status: str = "success" 