#pylint:disable=all
from src.data.use_cases.create_status import CreateStatus
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.repository.status_repository import StatusRepository
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from src.infra.relational.models.status import Status
from sqlalchemy import text
import pytest

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.commit()

@pytest.fixture
def db_connection_handler() -> DBConnectionHandler:
    return DBConnectionHandler(StringConnection())

@pytest.fixture
def create_status_case(db_connection_handler) -> CreateStatus:
    return CreateStatus(StatusRepository(db_connection_handler))

def test_create_status_case(db_connection_handler, create_status_case) -> None:
    create_status_case.create(
        description='my_description'
    )
    with db_connection_handler as db:
        select_status_script = text('''SELECT * FROM status''')
        result = db.session.execute(select_status_script)
        status_description = result.fetchone().description

    assert status_description == 'my_description'