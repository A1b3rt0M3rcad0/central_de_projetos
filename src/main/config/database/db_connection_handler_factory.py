from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection

def db_connection_handler_factory() -> DBConnectionHandler:
    return DBConnectionHandler(StringConnection())