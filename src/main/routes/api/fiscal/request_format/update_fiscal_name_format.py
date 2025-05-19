from pydantic import BaseModel

class UpdateFiscalNameFormat(BaseModel):
    name:str
    new_name:str