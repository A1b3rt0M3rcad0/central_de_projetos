from pydantic import BaseModel

class UpdateVerbaFormat(BaseModel):
    project_id:int
    verba_disponivel:float