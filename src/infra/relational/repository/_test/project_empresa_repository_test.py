from src.infra.relational.repository.project_empresa_repository import ProjectEmpresaRepository
from sqlalchemy import text
import pytest
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from datetime import datetime, timezone
from sqlalchemy import TextClause
from src.errors.repository.project_empresa_already_exists import ProjectEmpresaAlreadyExists
from src.errors.repository.projects_from_empresa_does_not_exists import ProjectsFromEmpresaDoesNotExists


@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project_type'))
        db.session.execute(text('DELETE FROM project_empresa'))
        db.session.execute(text('DELETE FROM refresh_token'))
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM user_project'))
        db.session.execute(text('DELETE FROM user'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.execute(text('DELETE FROM empresa'))
        db.session.commit()


@pytest.fixture
def insert_project_script() -> TextClause:
    return text('''
    insert into project (status_id, verba_disponivel, andamento_do_projeto, start_date, expected_completion_date, end_date) VALUES (:status_id, :verba_disponivel, :andamento_do_projeto, :start_date, :expected_completion_date, :end_date)
    ''')


@pytest.fixture
def insert_status_script() -> TextClause:
    return text('''INSERT INTO status (description, created_at) VALUES (:description, :created_at)''')


def test_insert(insert_project_script, insert_status_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_empresa_repository = ProjectEmpresaRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir empresa
        db.session.execute(
            text('INSERT INTO empresa (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'Empresa Teste', 'created_at': datetime.now(timezone.utc)}
        )

        empresa = db.session.execute(
            text('SELECT * FROM empresa WHERE name = :name'),
            {'name': 'Empresa Teste'}
        ).fetchone()

        # Inserir status
        db.session.execute(
            insert_status_script,
            {'description': 'Status Teste', 'created_at': datetime.now(timezone.utc)}
        )
        status = db.session.execute(
            text('SELECT * FROM status WHERE description = :description'),
            {'description': 'Status Teste'}
        ).fetchone()

        # Inserir projeto
        db.session.execute(
            insert_project_script,
            {
                'status_id': status.id,
                'verba_disponivel': 0,
                'andamento_do_projeto': datetime.now(timezone.utc),
                'start_date': datetime.now(timezone.utc),
                'expected_completion_date': datetime.now(timezone.utc),
                'end_date': datetime.now(timezone.utc)
            }
        )
        project = db.session.execute(
            text('SELECT * FROM project WHERE status_id = :status_id'),
            {'status_id': status.id}
        ).first()

        db.session.commit()

    # Inserir associação
    project_empresa_repository.insert(
        project_id=project.id,
        empresa_id=empresa.id
    )

    project_empresa = db.session.execute(
        text('''SELECT * FROM project_empresa WHERE project_id = :project_id AND empresa_id = :empresa_id'''),
        {
            'project_id': project.id,
            'empresa_id': empresa.id
        }
    ).first()

    assert project_empresa
    assert project_empresa.project_id == project.id
    assert project_empresa.empresa_id == empresa.id

    # Testando a exceção de já existir a associação
    with pytest.raises(ProjectEmpresaAlreadyExists):
        project_empresa_repository.insert(
            project_id=project.id,
            empresa_id=empresa.id
        )


def test_find_all_from_empresa(insert_project_script, insert_status_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_empresa_repository = ProjectEmpresaRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir empresa
        db.session.execute(
            text('INSERT INTO empresa (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'Empresa Teste Find', 'created_at': datetime.now(timezone.utc)}
        )
        empresa = db.session.execute(
            text('SELECT * FROM empresa WHERE name = :name'),
            {'name': 'Empresa Teste Find'}
        ).fetchone()

        # Inserir status
        db.session.execute(
            insert_status_script,
            {'description': 'Status Find', 'created_at': datetime.now(timezone.utc)}
        )
        status = db.session.execute(
            text('SELECT * FROM status WHERE description = :description'),
            {'description': 'Status Find'}
        ).fetchone()

        # Inserir projeto
        db.session.execute(
            insert_project_script,
            {
                'status_id': status.id,
                'verba_disponivel': 1000,
                'andamento_do_projeto': datetime.now(timezone.utc),
                'start_date': datetime.now(timezone.utc),
                'expected_completion_date': datetime.now(timezone.utc),
                'end_date': datetime.now(timezone.utc)
            }
        )
        project = db.session.execute(
            text('SELECT * FROM project WHERE status_id = :status_id'),
            {'status_id': status.id}
        ).fetchone()

        # Relacionar projeto à empresa
        db.session.execute(
            text('INSERT INTO project_empresa (project_id, empresa_id, created_at) VALUES (:project_id, :empresa_id, :created_at)'),
            {
                'project_id': project.id,
                'empresa_id': empresa.id,
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    # Teste de busca
    results = project_empresa_repository.find_all_from_empresa(empresa_id=empresa.id)

    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0].empresa_id == empresa.id
    assert results[0].project_id == project.id

    # Testar exceção para empresa sem projetos
    with pytest.raises(ProjectsFromEmpresaDoesNotExists):
        project_empresa_repository.find_all_from_empresa(empresa_id=9999)


def test_find(insert_project_script, insert_status_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_empresa_repository = ProjectEmpresaRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir empresa
        db.session.execute(
            text('INSERT INTO empresa (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'Empresa Teste Find', 'created_at': datetime.now(timezone.utc)}
        )
        empresa = db.session.execute(
            text('SELECT * FROM empresa WHERE name = :name'),
            {'name': 'Empresa Teste Find'}
        ).fetchone()

        # Inserir status
        db.session.execute(
            insert_status_script,
            {'description': 'Status Find', 'created_at': datetime.now(timezone.utc)}
        )
        status = db.session.execute(
            text('SELECT * FROM status WHERE description = :description'),
            {'description': 'Status Find'}
        ).fetchone()

        # Inserir projeto
        db.session.execute(
            insert_project_script,
            {
                'status_id': status.id,
                'verba_disponivel': 2000,
                'andamento_do_projeto': datetime.now(timezone.utc),
                'start_date': datetime.now(timezone.utc),
                'expected_completion_date': datetime.now(timezone.utc),
                'end_date': datetime.now(timezone.utc)
            }
        )
        project = db.session.execute(
            text('SELECT * FROM project WHERE status_id = :status_id'),
            {'status_id': status.id}
        ).fetchone()

        # Relacionar projeto à empresa
        db.session.execute(
            text('INSERT INTO project_empresa (project_id, empresa_id, created_at) VALUES (:project_id, :empresa_id, :created_at)'),
            {
                'project_id': project.id,
                'empresa_id': empresa.id,
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    # Teste de busca válida
    result = project_empresa_repository.find(empresa_id=empresa.id, project_id=project.id)

    assert result.project_id == project.id
    assert result.empresa_id == empresa.id
    assert isinstance(result.created_at, datetime)

    # Teste de exceção ao buscar associação inexistente
    with pytest.raises(ProjectsFromEmpresaDoesNotExists):
        project_empresa_repository.find(empresa_id=9999, project_id=9999)