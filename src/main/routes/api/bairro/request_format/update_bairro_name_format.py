from pydantic import BaseModel

class UpdateBairroNameFormat(BaseModel):
    name:str
    new_name:str