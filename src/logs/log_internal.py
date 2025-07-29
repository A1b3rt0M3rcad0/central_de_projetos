import inspect
from src.logs.logger.logger import logger
from datetime import datetime, timezone
from typing import Optional

def log_internal(logger_name: str, level: str, message: str, *, extra: Optional[dict] = None, func_name:str=None):
    """
    Loga informações de funções internas do sistema (controllers, repositories, utils, etc).

    Args:
        logger_name (str): Nome do logger.
        level (str): Nível do log (ex: 'INFO', 'ERROR').
        message (str): Mensagem principal do log.
        extra (dict, opcional): Informações adicionais para enriquecer o log.
        func_name (str, opcional): Nome da função que está gerando o log. Se não fornecido, será obtido do frame atual.
    """
    frame = inspect.currentframe().f_back
    logger(
        logger=logger_name,
        func_name=func_name if func_name else frame.f_code.co_name,
        lineno=frame.f_lineno,
        level=level,
        pathname=frame.f_code.co_filename,
        message=message if not extra else f"{message} | extra: {extra}",
        created=datetime.now(timezone.utc)
    )
