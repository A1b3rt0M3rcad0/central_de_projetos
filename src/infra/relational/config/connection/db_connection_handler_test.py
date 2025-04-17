import pytest
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
from sqlalchemy import text

@pytest.fixture
def url_connection() -> StringConnection:
    return StringConnection()

def test_db_connection_handler(url_connection) -> None:
    db_connection_handler = DBConnectionHandler(url_connection)
    with db_connection_handler as connection:
        result = connection.session.execute(text('SELECT 1'))
        value = result.scalar()

        assert value == 1