from fastapi.responses import JSONResponse
from src.presentation.http_types.http_response import HttpResponse

def response_adapter(http_response: HttpResponse) -> JSONResponse:
    return JSONResponse(
        status_code=http_response.status_code,
        content=http_response.body,
        headers=http_response.headers or {}
    )
