from pydantic import BaseModel

class UpdateTypeFormat(BaseModel):
    name:str
    new_name:str