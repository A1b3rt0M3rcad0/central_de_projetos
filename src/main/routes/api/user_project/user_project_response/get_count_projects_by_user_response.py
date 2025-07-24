from src.main.routes.api.__base_response.base_response import BaseResponse
from typing import Dict

class GetCountProjectsByUserResponse(BaseResponse[Dict[str, int]]):
    ...