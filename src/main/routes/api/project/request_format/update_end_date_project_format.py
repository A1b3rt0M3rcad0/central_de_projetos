from pydantic import BaseModel

class UpdateEndDateProjectFormat(BaseModel):
    project_id:int
    end_date:str