from pydantic import BaseModel
from typing import List, Optional, Union

class Errors(BaseModel):
    title: str
    detail: str

class ErrorResponse(BaseModel):
    errors: List[Errors]

def generate_error_responses(status_codes: Optional[List[Union[int, str]]] = None) -> dict:
    if not status_codes:
        return {
            "default": {
                "model": ErrorResponse
            }
        }

    return {
        code: {
            "model": ErrorResponse
        }
        for code in status_codes
    }