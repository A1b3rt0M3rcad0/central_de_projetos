from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler

def raven_connection_handler_factory() -> DBConnectionHandler:
    return DBConnectionHandler(
        data_connection=DataConnection()
    )