from pydantic import BaseModel, Field

class UpdateFiscalStatusFormat(BaseModel):
    is_active: int = Field(..., description="Status do fiscal (0 = inativo, 1 = ativo)", ge=0, le=1)

