#pylint:disable=all
import pytest
from datetime import datetime, timezone
from sqlalchemy import text

from src.data.use_cases.create_history_project import CreateHistoryProject
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError


from src.infra.relational.models.status import Status
from src.infra.relational.models.project import Project
from src.infra.relational.models.history_project import HistoryProject

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
def create_history_project_case(db_connection_handler) -> CreateHistoryProject:
    return CreateHistoryProject(HistoryProjectRepository(db_connection_handler))

def test_create_history_project_case(db_connection_handler, create_history_project_case) -> None:
    
    with db_connection_handler as db:
        create_status_script = text('''
                INSERT INTO status (description, created_at)
                VALUES (:description, :created_at)
            ''')
        db.session.execute(create_status_script, {
            'description': 'mydescription',
            'created_at': datetime.now(timezone.utc)
        })
        db.session.commit()

        find_status_script = text('SELECT * FROM status')
        result = db.session.execute(find_status_script).fetchone()
        status_id = result.id

        create_project_script = text('''
        insert into project (status_id, name) VALUES (:status_id, :name)
        ''')

        db.session.execute(create_project_script, {'status_id': status_id, 'name': 'pavimentacao'})

        db.session.commit()

        find_project_script = text(
            'SELECT * FROM project'
        )

        project_result = db.session.execute(find_project_script).fetchone()

        create_history_project_case.create(
            project_id=project_result.id,
            data_name='project.name',
            description='nome do projeto alterado para jose'
        )

        with pytest.raises(ProjectNotFoundError):
            create_history_project_case.create(
                project_id=-1,
                data_name='project.name',
                description='nome do projeto alterado para jose'
            )
