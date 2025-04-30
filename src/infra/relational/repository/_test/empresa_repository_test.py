import pytest
from sqlalchemy import text
from datetime import datetime, timezone

from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection


@pytest.fixture(autouse=True)
def cleanup_empresa():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project_type'))
        db.session.execute(text('DELETE FROM project_empresa'))
        db.session.execute(text('DELETE FROM empresa'))
        db.session.commit()


def test_insert_empresa():
    db_connection_handler = DBConnectionHandler(StringConnection())
    empresa_repository = EmpresaRepository(db_connection_handler)

    empresa_repository.insert(name='empresa_teste')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM empresa')).fetchone()

    assert result is not None
    assert result.name == 'empresa_teste'


def test_find_by_name_empresa():
    db_connection_handler = DBConnectionHandler(StringConnection())
    empresa_repository = EmpresaRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO empresa (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'empresa_teste', 'created_at': datetime.now(timezone.utc)}
        )
        db.session.commit()

    empresa = empresa_repository.find_by_name('empresa_teste')

    assert empresa
    assert empresa.name == 'empresa_teste'


def test_update_empresa():
    db_connection_handler = DBConnectionHandler(StringConnection())
    empresa_repository = EmpresaRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO empresa (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'empresa_teste', 'created_at': datetime.now(timezone.utc)}
        )
        db.session.commit()

    empresa_repository.update('empresa_teste', 'nova_empresa_teste')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM empresa')).fetchone()

    assert result
    assert result.name == 'nova_empresa_teste'


def test_delete_empresa():
    db_connection_handler = DBConnectionHandler(StringConnection())
    empresa_repository = EmpresaRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO empresa (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'empresa_teste', 'created_at': datetime.now(timezone.utc)}
        )
        db.session.commit()

    empresa_repository.delete('empresa_teste')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM empresa')).fetchone()

    assert not result