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