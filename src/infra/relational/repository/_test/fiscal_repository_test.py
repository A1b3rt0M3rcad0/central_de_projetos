from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
import pytest
from sqlalchemy import text
from datetime import datetime, timezone

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project_type'))
        db.session.execute(text('DELETE FROM project_empresa'))
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

def test_find_by_name() -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()
    
    fiscal = fiscal_repository.find_by_name('nome_teste')

    assert fiscal
    assert fiscal.name == 'nome_teste'

def test_update() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    fiscal_repository.update('nome_teste', 'new_nome_teste')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM fiscal')).fetchone()

    assert result
    assert result.name == 'new_nome_teste'

def test_delete() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    fiscal_repository.delete('nome_teste')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM fiscal')).fetchone()
    
    assert not result

def test_find_by_id() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    now = datetime.now(timezone.utc)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': now
            }
        )
        fiscal_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()
        db.session.commit()

    fiscal = fiscal_repository.find_by_id(fiscal_id)

    assert fiscal
    assert fiscal.fiscal_id == fiscal_id
    assert fiscal.name == 'nome_teste'