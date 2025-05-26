from src.presentation.http_types.http_response import HttpResponse
from src.errors.http.__http_base_error import HttpBaseError
from src.errors.use_cases.__base.base_use_case_error import BaseUseCaseError
from src.errors.repository.__base.base_repository_error import BaseRepositoryError
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
    if isinstance(error, BaseUseCaseError):
        return HttpResponse(
            status_code=500,
            body={
                'errors': [{
                    "title": error.title,
                    "message": error.message
                }]
            }
        )
    if isinstance(error, BaseRepositoryError):
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