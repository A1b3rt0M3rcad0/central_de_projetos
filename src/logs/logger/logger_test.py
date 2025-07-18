from src.logs.logger.logger import logger
from datetime import datetime, timezone

def test_save() -> None:
    logger(
        logger="asdf",
        func_name="Test Logger",
        level="INFO",
        lineno=0,
        pathname="logger_path",
        message="OLÀ MUNDO",
        created=datetime.now(timezone.utc)
    )