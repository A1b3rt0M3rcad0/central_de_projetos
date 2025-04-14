from src.infra.relational.repository.status_repository import StatusRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
from sqlalchemy import text
from datetime import datetime, timezone
import pytest

@pytest.fixture
def description() -> str:
    return f'''{'This is a long description'*7}'''


def test_insert_status(description) -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    status_repository = StatusRepository(db_connection_handler)

    status_repository.insert(description=description)

    with db_connection_handler as db:

        find_script = text('select * from status where description= :description')

        result = db.session.execute(find_script, {'description': description}).fetchone()

        assert result.description == description

        delete_script = text('delete from status where id >= 1;')
        db.session.execute(delete_script)

        db.session.commit()

def test_find_status(description) -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    status_repository = StatusRepository(db_connection_handler)

    with db_connection_handler as db:

        insert_script = text('''insert into status (description, created_at) values (:description, :created_at)''')

        now = datetime.now(timezone.utc)

        db.session.execute(insert_script, {
            'description': description,
            'created_at': now
        })

        db.session.commit()

        # description find
        result = status_repository.find(description=description)

        assert result.description == description

        result2 = status_repository.find(status_id=result.status_id)

        assert result2.description == description

        result3 = status_repository.find(status_id=result.status_id, description=description)

        assert result3.description == description

        delete_script = text('delete from status where id >= 1;')
        db.session.execute(delete_script)

        db.session.commit()

def test_find_all_status(description) -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    status_repository = StatusRepository(db_connection_handler)

    with db_connection_handler as db:

        insert_script = text('''insert into status (description, created_at) values (:description, :created_at)''')

        now = datetime.now(timezone.utc)

        db.session.execute(insert_script, {
            'description': description + '0',
            'created_at': now
        })

        db.session.execute(insert_script, {
            'description': description + '1',
            'created_at': now
        })


        db.session.execute(insert_script, {
            'description': description + '2',
            'created_at': now
        })

        db.session.commit()

        results = status_repository.find_all()

        assert len(results) == 3

        for i, status_entity in enumerate(results):
            assert status_entity.description == description + f'{i}'

        delete_script = text('delete from status where id >= 1;')
        db.session.execute(delete_script)
        db.session.commit()

def test_update_status(description) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    status_repository = StatusRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserção inicial de um status
        insert_script = text('''INSERT INTO status (description, created_at) VALUES (:description, :created_at)''')
        now = datetime.now(timezone.utc)
        db.session.execute(insert_script, {
            'description': description,
            'created_at': now
        })
        db.session.commit()

        # Buscar o registro recém inserido para obter o ID
        select_script = text('SELECT * FROM status WHERE description = :description')
        result = db.session.execute(select_script, {'description': description}).fetchone()
        assert result is not None

        # Realizar o update usando o repositório
        updated_description = "Updated description"
        status_repository.update(
            update_params={"description": updated_description},
            status_id=result.id
        )

        # Buscar novamente para verificar se foi atualizado
        updated_result = db.session.execute(
            text('SELECT * FROM status WHERE id = :id'),
            {'id': result.id}
        ).fetchone()

        assert updated_result is not None
        assert updated_result.description == updated_description

        # Cleanup
        delete_script = text('DELETE FROM status WHERE id >= 1')
        db.session.execute(delete_script)
        db.session.commit()
