import pytest
from sqlalchemy import text
from datetime import datetime, timezone

from src.infra.relational.repository.bairro_repository import BairroRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from src.errors.repository.not_exists_error.bairro_not_exists import BairroNotExists
from src.errors.repository.already_exists_error.bairro_already_exists import BairroAlreadyExists

@pytest.fixture(autouse=True)
def cleanup_bairro_table():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project_type'))
        db.session.execute(text('DELETE FROM project_empresa'))
        db.session.execute(text('DELETE FROM bairro'))
        db.session.commit()

def test_insert_bairro() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    bairro_repository = BairroRepository(db_connection_handler)

    bairro_repository.insert(name='bairro_teste')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM bairro')).fetchone()

    assert result is not None
    assert result.name == 'bairro_teste'

def test_insert_bairro_already_exists_error() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    bairro_repository = BairroRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO bairro (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'bairro_teste', 'created_at': datetime.now(timezone.utc)}
        )
        db.session.commit()

    with pytest.raises(BairroAlreadyExists):
        bairro_repository.insert(name='bairro_teste')

def test_find_by_name_success() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    bairro_repository = BairroRepository(db_connection_handler)

    now = datetime.now(timezone.utc)
    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO bairro (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'bairro_teste', 'created_at': now}
        )
        db.session.commit()

    bairro = bairro_repository.find_by_name('bairro_teste')

    assert bairro is not None
    assert bairro.name == 'bairro_teste'

def test_find_by_name_not_found() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    bairro_repository = BairroRepository(db_connection_handler)

    with pytest.raises(BairroNotExists):
        bairro_repository.find_by_name('inexistente')

def test_update_bairro() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    bairro_repository = BairroRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO bairro (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'bairro_antigo', 'created_at': datetime.now(timezone.utc)}
        )
        db.session.commit()

    bairro_repository.update(name='bairro_antigo', new_name='bairro_novo')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM bairro')).fetchone()

    assert result.name == 'bairro_novo'

def test_delete_bairro() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    bairro_repository = BairroRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO bairro (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'bairro_para_deletar', 'created_at': datetime.now(timezone.utc)}
        )
        db.session.commit()

    bairro_repository.delete(name='bairro_para_deletar')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM bairro')).fetchone()

    assert result is None

def test_find_by_id_success() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    bairro_repository = BairroRepository(db_connection_handler)

    now = datetime.now(timezone.utc)
    with db_connection_handler as db:
        # Inserir o bairro
        db.session.execute(
            text('INSERT INTO bairro (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'bairro_id_teste', 'created_at': now}
        )
        db.session.commit()

        # Buscar o ID do bairro recém-inserido
        result = db.session.execute(
            text('SELECT id FROM bairro WHERE name = :name'),
            {'name': 'bairro_id_teste'}
        ).fetchone()
        inserted_id = result.id

    # Testar o método find_by_id
    bairro = bairro_repository.find_by_id(inserted_id)

    assert bairro is not None
    assert bairro.bairro == inserted_id
    assert bairro.name == 'bairro_id_teste'

def test_find_by_id_not_found() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    bairro_repository = BairroRepository(db_connection_handler)

    with pytest.raises(BairroNotExists):
        bairro_repository.find_by_id(9999)  # ID que sabemos que não existe