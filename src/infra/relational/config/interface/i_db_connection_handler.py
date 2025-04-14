
from abc import ABC, abstractmethod
from sqlalchemy import Engine
from sqlalchemy.orm import Session

class IDBConnectionHandler(ABC):

    @property
    @abstractmethod
    def session(self) -> Session:pass

    @abstractmethod
    def get_engine(self) -> Engine:pass