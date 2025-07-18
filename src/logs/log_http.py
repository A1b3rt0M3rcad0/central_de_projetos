import inspect
from src.logs.logger.logger import logger
from datetime import datetime, timezone
from src.logs.sanitize import sanitize
from fastapi import Request
from src.presentation.http_types.http_response import HttpResponse

def log_http(logger_name:str, level: str, http_response:HttpResponse, request:Request):
    frame = inspect.currentframe().f_back
    logger(
        logger=logger_name,
        func_name=frame.f_code.co_name,
        lineno=frame.f_lineno,
        level=level,
        pathname=frame.f_code.co_filename,
        message=f"request:\nmethod: {request.method}, response:\nstatus: {http_response.status_code}, body: {sanitize(http_response.body)}",
        created=datetime.now(timezone.utc)
    )