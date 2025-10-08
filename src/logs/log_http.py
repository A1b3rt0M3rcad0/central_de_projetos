import inspect
from src.logs.logger.logger import logger
from datetime import datetime, timezone
from src.logs.sanitize import sanitize
from fastapi import Request
from src.presentation.http_types.http_response import HttpResponse
from typing import Optional

def log_http(logger_name:str, level: str, http_response:HttpResponse, request:Request, message:Optional[str]=None):
    frame = inspect.currentframe().f_back
    
    # Tratar body bytes (arquivos/documentos)
    if isinstance(http_response.body, bytes):
        body_info = f"<binary data, {len(http_response.body)} bytes>"
    elif isinstance(http_response.body, dict):
        body_info = sanitize(http_response.body)
    else:
        body_info = http_response.body
    
    logger(
        logger=logger_name,
        func_name=frame.f_code.co_name,
        lineno=frame.f_lineno,
        level=level,
        pathname=frame.f_code.co_filename,
        message=message if message else f"request:\nmethod: {request.method}\nresponse:\nstatus: {http_response.status_code}, body: {body_info}",
        created=datetime.now(timezone.utc)
    )