import os
import dotenv
from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional
from src.infra.mongo.config.connection.interface.i_string_connection import IStringConnection
from src.infra.mongo.config.connection.interface.i_db_connection_handler import IDBConnectionHandler

class DBConnectionHandler(IDBConnectionHandler):

    def __init__(self, connection: IStringConnection):
        dotenv.load_dotenv()
        self.__connection = connection.string
        self.__database_name = os.getenv("DB_NAME")
        self.__client:Optional[MongoClient] = None
        self.__db_connection:Optional[Database] = None

    def _connect_to_db(self) -> None:
        self.__client = MongoClient(self.__connection)
        self.__db_connection = self.__client[self.__database_name]
    
    def __enter__(self) -> Database:
        self._connect_to_db()
        return self.__db_connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client.close()
        self.__db_connection = None
        self.__client = None