from src.infra.mongo.models.log_entry_model import LogEntryModel
from datetime import datetime, timezone

def log_format_factory(
    level: str = "INFO",
    message: str = "",
    created: datetime = None,
    func_name: str = "",
    lineno: int = 0,
    logger: str = "default",
    pathname: str = ""
) -> LogEntryModel:
    return LogEntryModel(
        level=level,
        message=message,
        created=created or datetime.now(timezone.utc),
        funcName=func_name,
        lineno=lineno,
        logger=logger,
        pathname=pathname
    )
