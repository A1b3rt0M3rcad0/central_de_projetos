from pydantic import BaseModel

class UpdateStartDateFormat(BaseModel):
    project_id:int
    start_date:str