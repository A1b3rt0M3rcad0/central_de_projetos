import inspect
from src.logs.logger.logger import logger
from datetime import datetime, timezone
from src.logs.sanitize import sanitize
from typing import Dict

def log_http(logger_name:str, level: str, http_response:Dict):
    frame = inspect.currentframe().f_back
    logger(
        logger=logger_name,
        func_name=frame.f_code.co_name,
        lineno=frame.f_lineno,
        level=level,
        pathname=frame.f_code.co_filename,
        message=f"response:\nstatus: {http_response.status_code}, body: {sanitize(http_response.body)}",
        created=datetime.now(timezone.utc)
    )