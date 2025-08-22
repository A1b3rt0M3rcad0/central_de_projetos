#pylint:disable=W0718
from fastapi import Request as FastAPIRequest
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

async def set_cached_adapter(http_response:HttpResponse, framework_request:FastAPIRequest, controller: Callable[[HttpRequest], HttpResponse]) -> HttpResponse:
    # Convert HttpResponse and FastAPIRequest one to HttpRequest
    http_request = HttpRequest(
        body=http_response.body,
        headers=dict(framework_request.headers),
        query_params=dict(framework_request.query_params),
        path_params=framework_request.path_params,
        url=str(framework_request.url),
    )

    # Call the controller with the adapted request
    response: HttpResponse = controller(http_request)

    return response
