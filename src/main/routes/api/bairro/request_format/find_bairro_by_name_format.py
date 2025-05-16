from pydantic import BaseModel

class FindBairroByNameFormat(BaseModel):
    bairro_name:str