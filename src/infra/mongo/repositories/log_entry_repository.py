from src.infra.mongo.config.connection.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.mongo.models.log_entry_model import LogEntryModel
from src.data.interface.i_log_entry_repository import ILogEntryRepository
from src.infra.mongo.documents.log_document import LogDocument
from pymongo.errors import DuplicateKeyError
from typing import List

class LogEntryRepository(ILogEntryRepository):

    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
        self.__log_document = LogDocument(db_connection_handler)

    def save(self, log: LogEntryModel) -> None:
        try:
            with self.__db_connection_handler as db:
                if db is not None:
                    db[self.__log_document.document].insert_one(log.model_dump())
                    return
                raise ValueError("Database connection is None")
        except DuplicateKeyError as e:
            raise ValueError("This log entry already exists") from e
        except Exception as e:
            raise e

    def find_all(self, limit: int = 100) -> List[LogEntryModel]:
        try:
            with self.__db_connection_handler as db:
                if db is not None:
                    cursor = db[self.__log_document.document].find().sort("created", -1).limit(limit)
                    return [LogEntryModel(**doc) for doc in cursor]
                raise ValueError("Database connection is None")
        except Exception as e:
            raise e