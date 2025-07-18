from src.infra.mongo.config.connection.string_connection import StringConnection
from src.infra.mongo.config.connection.db_connection_handler import DBConnectionHandler

def mongo_server_handler_composer() -> DBConnectionHandler:
    return DBConnectionHandler(StringConnection())