from ravendb import DocumentStore
from ravendb import DocumentSession
from src.infra.raven.config.connection.interface.i_data_connection import IDataConnection
from typing import Optional


class DBConnectionHandler:

    def __init__(self, data_connection:IDataConnection) -> None:
        self.data_connection = data_connection
        self.engine:Optional[DocumentStore] = None
        self.session:Optional[DocumentSession] = None
    
    def __create_engine(self) -> DocumentStore:
        return DocumentStore(**self.data_connection.data())
    
    def __enter__(self) -> DocumentSession:
        self.engine = self.__create_engine()
        self.engine.initialize()
        self.session = self.engine.open_session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.session:
            self.session.save_changes()
            self.session = None
        self.engine.close()