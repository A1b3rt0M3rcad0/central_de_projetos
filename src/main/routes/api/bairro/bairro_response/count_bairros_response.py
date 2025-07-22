from pydantic import BaseModel
from src.main.routes.api.__base_response.base_response import BaseResponse

class CountBairrosContent(BaseModel):
    bairros:int

class CountBairrosResponse(BaseResponse[CountBairrosContent]):
    ...