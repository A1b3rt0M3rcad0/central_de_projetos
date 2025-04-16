from pymongo.database import Database
from abc import ABC, abstractmethod
from src.infra.mongo.config.connection.interface.i_string_connection import IStringConnection

class IDBConnectionHandler(ABC):

    @abstractmethod
    def __init__(self, connection: IStringConnection):pass

    @abstractmethod
    def _connect_to_db(self) -> None:pass

    @abstractmethod
    def __enter__(self) -> Database:pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):pass