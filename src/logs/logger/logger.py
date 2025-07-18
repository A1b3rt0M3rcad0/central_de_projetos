from src.logs.config.mongo_server_handler_composer import mongo_server_handler_composer
from src.infra.mongo.repositories.log_entry_repository import LogEntryRepository
from src.logs.config.log_format_factory import log_format_factory
from src.logs.config.log_handler import LogHandler
from datetime import datetime

def logger(
    level: str = "INFO",
    message: str = "",
    created: datetime = None,
    func_name: str = "",
    lineno: int = 0,
    logger: str = "default",
    pathname: str = ""
) -> None:
    log_handler = LogHandler(
        log_entry_repository=LogEntryRepository(
            db_connection_handler=mongo_server_handler_composer()
        )
    )
    log_model = log_format_factory(
        level=level,
        pathname=pathname,
        message=message,
        func_name=func_name,
        logger=logger,
        lineno=lineno,
        created=created
    )
    log_handler.save(log_model)