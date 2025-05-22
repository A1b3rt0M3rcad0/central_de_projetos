from fastapi import UploadFile, File
from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


async def file_adapter(
    file: UploadFile = File(...), 
    controller: Callable[[HttpRequest], HttpResponse] = None,
    **kwargs:dict
) -> HttpResponse:
    
    if not controller:
        raise ValueError('Need File Controller')

    content = await file.read()

    http_request = HttpRequest(
    body={
        'document': content,
        'document_name': file.filename,
        'name': file.filename,
        'content_type': file.content_type,
        **kwargs  # espalha kwargs dentro do dict
        }
    )

    http_response = controller(http_request)
    return http_response