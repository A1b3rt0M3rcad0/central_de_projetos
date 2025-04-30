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
        db.session.execute(text('DELETE FROM project_type'))
        db.session.execute(text('DELETE FROM project_empresa'))
        db.session.execute(text('DELETE FROM project_fiscal'))
        db.session.execute(text('DELETE FROM history_project'))
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

def test_find(
    monetary_value, 
    andamento_do_projeto, 
    datetime_fixture, 
    insert_status_script, 
    select_status_script, 
    insert_project_script
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_repository = ProjectRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir o status
        db.session.execute(insert_status_script, {
            'description': 'description_too_long',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(select_status_script).first()

        # Inserir projeto com o status_id recém-criado
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'verba_disponivel': monetary_value.value,
            'andamento_do_projeto': andamento_do_projeto,
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': datetime_fixture
        })
        db.session.commit()

        # Recuperar ID do projeto inserido
        result = db.session.execute(text("SELECT id FROM project WHERE status_id = :status_id"), {'status_id': status.id}).first()
        project_id = result.id

    # Buscar o projeto usando o repositório
    project = project_repository.find(project_id)

    assert project.project_id == project_id
    assert project.status_id == status.id
    assert project.verba_disponivel == monetary_value.value
    assert project.andamento_do_projeto == andamento_do_projeto

def test_find_all(
    monetary_value,
    andamento_do_projeto,
    datetime_fixture,
    insert_status_script,
    select_status_script,
    insert_project_script
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_repository = ProjectRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Test Status',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(select_status_script).first()

        # Inserir dois projetos
        for _ in range(2):
            db.session.execute(insert_project_script, {
                'status_id': status.id,
                'verba_disponivel': monetary_value.value,
                'andamento_do_projeto': andamento_do_projeto,
                'start_date': datetime_fixture,
                'expected_completion_date': datetime_fixture,
                'end_date': datetime_fixture
            })
        db.session.commit()

    # Buscar todos os projetos
    result = project_repository.find_all()

    assert isinstance(result, list)
    assert len(result) == 2

    for project in result:
        assert project.status_id == status.id
        assert project.verba_disponivel == monetary_value.value
        assert project.andamento_do_projeto == andamento_do_projeto

def test_find_by_status(
    monetary_value,
    andamento_do_projeto,
    datetime_fixture,
    insert_status_script,
    select_status_script,
    insert_project_script
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_repository = ProjectRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Test Status',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(select_status_script).first()

        # Inserir dois projetos
        for _ in range(2):
            db.session.execute(insert_project_script, {
                'status_id': status.id,
                'verba_disponivel': monetary_value.value,
                'andamento_do_projeto': andamento_do_projeto,
                'start_date': datetime_fixture,
                'expected_completion_date': datetime_fixture,
                'end_date': datetime_fixture
            })
        db.session.commit()

    # Buscar todos os projetos pelo status
    result = project_repository.find_by_status(status.id)

    assert isinstance(result, list)
    assert len(result) == 2

    for project in result:
        assert project.status_id == status.id
        assert project.verba_disponivel == monetary_value.value
        assert project.andamento_do_projeto == andamento_do_projeto

def test_update(monetary_value,
    andamento_do_projeto,
    datetime_fixture,
    insert_status_script,
    select_status_script,
    insert_project_script,
    select_project_script
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_repository = ProjectRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Test Status',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(select_status_script).first()

        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'verba_disponivel': monetary_value.value,
            'andamento_do_projeto': andamento_do_projeto,
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': datetime_fixture
            })
        db.session.commit()

        project = db.session.execute(select_project_script, {'status_id': status.id}).first()
        project_id = project.id
        project_verba = project.verba_disponivel

        project_repository.update(project_id, {'verba_disponivel': 2000})

        project_updated = db.session.execute(select_project_script, {'status_id': status.id}).first()
        
        assert project_updated.verba_disponivel != project_verba
        assert project_updated.verba_disponivel == 2000

def test_delete(monetary_value,
    andamento_do_projeto,
    datetime_fixture,
    insert_status_script,
    select_status_script,
    insert_project_script,
    select_project_script
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_repository = ProjectRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Test Status',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(select_status_script).first()

        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'verba_disponivel': monetary_value.value,
            'andamento_do_projeto': andamento_do_projeto,
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': datetime_fixture
            })
        db.session.commit()

        project = db.session.execute(select_project_script, {'status_id': status.id}).first()
        project_id = project.id

        project_repository.delete(project_id)

        project = db.session.execute(select_project_script, {'status_id': status.id}).first()

        assert project is None