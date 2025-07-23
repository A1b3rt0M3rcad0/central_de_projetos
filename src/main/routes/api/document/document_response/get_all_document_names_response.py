from src.main.routes.api.__base_response.base_response import BaseResponse
from typing import List

class GetAllDocumentNamesResponse(BaseResponse[List[str]]):
    ...