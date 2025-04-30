from src.infra.relational.repository.types_repository import TypesRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
import pytest
from sqlalchemy import text
from datetime import datetime, timezone


@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM types'))
        db.session.commit()


def test_insert_types() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    types_repository = TypesRepository(db_connection_handler)

    types_repository.insert(name='tipo_teste')

    with db_connection_handler as db:
        result = db.session.execute(
            text('SELECT * FROM types')
        ).fetchone()

    assert result is not None
    assert result.name == 'tipo_teste'


def test_find_by_name_types() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    types_repository = TypesRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO types (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'tipo_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    types_entity = types_repository.find_by_name('tipo_teste')

    assert types_entity
    assert types_entity.name == 'tipo_teste'


def test_update_types() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    types_repository = TypesRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO types (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'tipo_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    types_repository.update('tipo_teste', 'novo_tipo_teste')

    with db_connection_handler as db:
        result = db.session.execute(
            text('SELECT * FROM types')
        ).fetchone()

    assert result
    assert result.name == 'novo_tipo_teste'


def test_delete_types() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    types_repository = TypesRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO types (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'tipo_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    types_repository.delete('tipo_teste')

    with db_connection_handler as db:
        result = db.session.execute(
            text('SELECT * FROM types')
        ).fetchone()

    assert not result