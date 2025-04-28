from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
import pytest
from sqlalchemy import text

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM fiscal'))
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.commit()

def test_insert_fiscal() -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    fiscal_repository.insert(name='nome_teste')

    with db_connection_handler as db:
        result = db.session.execute(
            text('SELECT * FROM fiscal')
        ).fetchone()
    
    assert result is not None
    assert result.name == 'nome_teste'
