
from abc import ABC, abstractmethod
from sqlalchemy import Engine

class IDBConnectionHandler(ABC):

    @abstractmethod
    def get_engine(self) -> Engine:pass