from pydantic import BaseModel

class UpdateExpectedCompletionDateFormat(BaseModel):
    project_id:int
    expected_completion_date:str