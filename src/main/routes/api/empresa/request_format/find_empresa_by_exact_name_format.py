from pydantic import BaseModel

class FindEmpresaByExactNameFormat(BaseModel):
    empresa_name:str