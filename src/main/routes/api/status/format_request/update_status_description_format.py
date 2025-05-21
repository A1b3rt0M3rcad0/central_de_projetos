from pydantic import BaseModel

class UpdateStatusDescriptionFormat(BaseModel):
    status_id:int
    description:str