from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    message:str
    content:T
    access_token:Optional[str]