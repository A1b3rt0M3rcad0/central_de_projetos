from src.infra.relational.repository.status_repository import StatusRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
from sqlalchemy import text
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