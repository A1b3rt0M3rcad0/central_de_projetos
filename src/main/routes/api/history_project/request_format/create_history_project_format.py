from pydantic import BaseModel

class CreateHistoryProjectFormat(BaseModel):
    project_id:int
    data_name:str
    description:str