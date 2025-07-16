from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class LogEntryModel(BaseModel):
    level: str
    message: str
    logger: str
    pathname: Optional[str]
    lineno: Optional[int]
    funcName: Optional[str]
    created: datetime = Field(default_factory=datetime.now(timezone.utc))