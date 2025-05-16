from src.presentation.http_types.http_response import HttpResponse
from src.errors.http.__http_base_error import HttpBaseError
from src.errors.use_cases.base.BaseError import BaseError

def error_handler(error: Exception) -> HttpResponse:

    if isinstance(error, HttpBaseError):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.title,
                    "detail": error.message
                }]
            }
        )
    if isinstance(error, BaseError):
        return HttpResponse(
            status_code=500,
            body={
                'errors': [{
                    "title": error.title,
                    "message": error.message
                }]
            }
        )
    return HttpResponse(
        status_code=500,
        body = {
            "errors": [{
                "title": "Internal Server Error",
                "detail": str(error)
            }]
        }
    )