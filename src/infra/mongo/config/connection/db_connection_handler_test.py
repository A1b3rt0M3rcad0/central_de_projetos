# pylint: disable=W0212,W0613
import pytest
from unittest.mock import MagicMock, patch
from pymongo import MongoClient
from src.infra.mongo.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.mongo.config.connection.interface.i_string_connection import IStringConnection


class MockStringConnection(IStringConnection):
    def __init__(self, connection_string: str, db_name: str):
        self._string = connection_string
        self._db_name = db_name

    @property
    def string(self) -> str:
        return self._string

    def database_name(self) -> str:
        return self._db_name


@pytest.fixture
def mock_string_connection():
    return MockStringConnection('mongodb://localhost:27017', 'test_db')


@pytest.fixture
def mock_mongo_client():
    mock_client = MagicMock(spec=MongoClient)
    mock_db = MagicMock()
    mock_client.__getitem__.return_value = mock_db
    return mock_client


def test_init_connection_handler(mock_string_connection):
    handler = DBConnectionHandler(mock_string_connection)
    assert handler._DBConnectionHandler__connection == 'mongodb://localhost:27017'
    assert handler._DBConnectionHandler__database_name == 'test_db'
    assert handler._DBConnectionHandler__client is None
    assert handler._DBConnectionHandler__db_connection is None


@patch('src.infra.mongo.config.connection.db_connection_handler.MongoClient')
def test_connect_to_db(mock_mongo_client_class, mock_string_connection):
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_client.__getitem__.return_value = mock_db
    mock_mongo_client_class.return_value = mock_client

    handler = DBConnectionHandler(mock_string_connection)
    handler._connect_to_db()

    mock_mongo_client_class.assert_called_once_with('mongodb://localhost:27017')
    mock_client.__getitem__.assert_called_once_with('test_db')
    assert handler._DBConnectionHandler__client == mock_client
    assert handler._DBConnectionHandler__db_connection == mock_db


@patch('src.infra.mongo.config.connection.db_connection_handler.MongoClient')
def test_context_manager(mock_mongo_client_class, mock_string_connection):
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_client.__getitem__.return_value = mock_db
    mock_mongo_client_class.return_value = mock_client

    handler = DBConnectionHandler(mock_string_connection)

    with handler as db:
        assert db == mock_db
        assert handler._DBConnectionHandler__client == mock_client
        assert handler._DBConnectionHandler__db_connection == mock_db

    mock_client.close.assert_called_once()
    assert handler._DBConnectionHandler__client is None
    assert handler._DBConnectionHandler__db_connection is None
