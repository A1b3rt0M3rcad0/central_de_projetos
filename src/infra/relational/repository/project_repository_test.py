from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime, timezone
from sqlalchemy import text, TextClause
from src.infra.relational.repository.project_repository import ProjectRepository
import pytest

@pytest.fixture
def monetary_value() -> MonetaryValue:
    return MonetaryValue(10_000)

@pytest.fixture
def andamento_do_projeto() -> str:
    return 'Fase de Protótipo'

@pytest.fixture
def datetime_fixture() -> datetime:
    return datetime.now(timezone.utc)

@pytest.fixture
def insert_project_script() -> TextClause:
    return text('''
    insert into project (status_id, verba_disponivel, andamento_do_projeto, start_date, expected_completion_date, end_date) VALUES (:status_id, :verba_disponivel, :andamento_do_projeto, :start_date, :expected_completion_date, :end_date)
    ''')

@pytest.fixture
def select_project_script() -> TextClause:
    return text('''
    select * from project where status_id = :status_id
    ''')

@pytest.fixture
def insert_status_script() -> TextClause:
    return text('''INSERT INTO status (description, created_at) VALUES (:description, :created_at)''')

@pytest.fixture
def select_status_script() -> TextClause:
    return text('SELECT * FROM status')

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.commit()

def test_insert(monetary_value, andamento_do_projeto, datetime_fixture, select_project_script, insert_status_script, select_status_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_repository = ProjectRepository(db_connection_handler)
    with db_connection_handler as db:
        db.session.execute(insert_status_script, {
            'description': 'description_too_long',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(select_status_script).first()

        project_repository.insert(
            status_id=status.id, 
            verba_disponivel=monetary_value, andamento_do_projeto=andamento_do_projeto, start_date=datetime_fixture, expected_completion_date=datetime_fixture, end_date=datetime_fixture
        )

        project = db.session.execute(select_project_script, {'status_id': status.id}).first()

        assert project.verba_disponivel == monetary_value.value
        assert project.andamento_do_projeto  == andamento_do_projeto
        assert project.status_id == status.id

        