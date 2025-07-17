import pytest
from datetime import datetime, timezone

from src.infra.mongo.models.log_entry_model import LogEntryModel
from src.infra.mongo.repositories.log_entry_repository import LogEntryRepository
from src.infra.mongo.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.mongo.config.connection.t_string_connection import TStringConnection

@pytest.fixture
def db_connection_handler() -> DBConnectionHandler:
    return DBConnectionHandler(TStringConnection())

@pytest.fixture
def log_entry() -> LogEntryModel:
    return LogEntryModel(
        level="INFO",
        message="Test log message",
        logger="test_logger",
        pathname="/app/test.py",
        lineno=42,
        funcName="test_function",
        created=datetime.now(timezone.utc)
    )

def test_save_log_entry(db_connection_handler, log_entry):
    repository = LogEntryRepository(db_connection_handler)

    # Salva o log
    repository.save(log_entry)

    # Verifica se o log foi salvo no MongoDB
    with db_connection_handler as db:
        if db is not None:
            result = db['logdocument'].find_one({"message": "Test log message"})
            assert result is not None
            assert result["level"] == "INFO"
            assert result["logger"] == "test_logger"

def test_find_all_logs(db_connection_handler):
    repository = LogEntryRepository(db_connection_handler)

    # Insere múltiplos logs
    for i in range(5):
        log = LogEntryModel(
            level="DEBUG",
            message=f"Mensagem {i}",
            logger="bulk_logger",
            pathname=f"/tmp/{i}.py",
            lineno=i,
            funcName=f"func_{i}",
            created=datetime.now(timezone.utc)
        )
        repository.save(log)

    # Recupera os logs
    logs = repository.find_all(limit=3)

    assert len(logs) == 3
    assert all(isinstance(log, LogEntryModel) for log in logs)
    assert all(log.logger == "bulk_logger" for log in logs)
