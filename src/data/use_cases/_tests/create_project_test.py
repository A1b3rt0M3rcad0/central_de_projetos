#pylint:disable=all
import pytest
from datetime import datetime, timezone
from sqlalchemy import text

from src.data.use_cases.create_project import CreateProject
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.domain.value_objects.monetary_value import MonetaryValue

from src.infra.relational.models.status import Status
from src.infra.relational.models.project import Project

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.commit()

@pytest.fixture
def db_connection_handler():
    return DBConnectionHandler(StringConnection())

@pytest.fixture
def create_project_case(db_connection_handler):
    return CreateProject(ProjectRepository(db_connection_handler))

def test_create_project_case(create_project_case, db_connection_handler):
    with db_connection_handler as db:
        # Cria status
        create_status_script = text('''
            INSERT INTO status (description, created_at)
            VALUES (:description, :created_at)
        ''')
        db.session.execute(create_status_script, {
            'description': 'mydescription',
            'created_at': datetime.now(timezone.utc)
        })
        db.session.commit()

        # Recupera ID do status
        find_status_script = text('SELECT id FROM status')
        result = db.session.execute(find_status_script)
        status_id = result.scalar()

    # Cria projeto usando o caso de uso
    create_project_case.create(
        status_id=status_id,
        name='pavimentação',
        verba_disponivel=MonetaryValue(12123123123),
        andamento_do_projeto='Em fase de entrega',
    )

    # Verifica se projeto foi criado
    with db_connection_handler as db:
        result = db.session.execute(text('SELECT name FROM project'))
        project_name = result.scalar()

    assert project_name == 'pavimentação'