
from abc import ABC, abstractmethod
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from typing import Self

class IDBConnectionHandler(ABC):

    @property
    @abstractmethod
    def session(self) -> Session:pass

    @abstractmethod
    def get_engine(self) -> Engine:pass

    def __enter__(self) -> Self:pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:pass