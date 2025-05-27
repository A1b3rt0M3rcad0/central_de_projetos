from src.presentation.http_types.http_response import HttpResponse
from src.errors.http.__http_base_error import HttpBaseError
from src.errors.use_cases.__base.base_use_case_error import BaseUseCaseError

# 409 errors
from src.errors.repository.already_exists_error.__base_already_exists_error import BaseAlreadyExistsError
from src.errors.repository.has_related_children.__base_has_related_children import BaseHasRelatedChildren

# 404 errors
from src.errors.repository.not_exists_error.__base_not_exists_error import BaseNotExistsError

# 500 errors
from src.errors.repository.error_on_delete.__base_error_on_delete import BaseErrorOnDelete
from src.errors.repository.error_on_find.__base_error_on_find import BaseErrorOnFind
from src.errors.repository.error_on_insert.__base_error_on_insert import BaseErrorOnInsert
from src.errors.repository.error_on_update.__base_error_on_update import BaseErrorOnUpdate


def format_error_response(status_code: int, title: str, detail: str) -> HttpResponse:
    return HttpResponse(
        status_code=status_code,
        body={
            "errors": [{
                "title": title,
                "detail": detail
            }]
        }
    )


def error_handler(error: Exception) -> HttpResponse:

    if isinstance(error, HttpBaseError):
        return format_error_response(
            status_code=error.status_code,
            title=error.title,
            detail=error.message
        )

    ERROR_STATUS_MAPPING = {
        BaseAlreadyExistsError: 409,
        BaseHasRelatedChildren: 409,
        BaseNotExistsError: 404,
        BaseUseCaseError: 500,
        BaseErrorOnInsert: 500,
        BaseErrorOnFind: 500,
        BaseErrorOnUpdate: 500,
        BaseErrorOnDelete: 500
    }

    for exc_type, status_code in ERROR_STATUS_MAPPING.items():
        if isinstance(error, exc_type):
            return format_error_response(
                status_code=status_code,
                title=error.title,
                detail=error.message
            )

    return format_error_response(
        status_code=500,
        title="Internal Server Error",
        detail=str(error)
    )