from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from sqlalchemy import text
import pytest
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from datetime import datetime, timezone
from sqlalchemy import TextClause
from src.errors.repository.project_fiscal_already_exists import ProjectFiscalAlreadyExists
from src.errors.repository.projects_from_fiscal_does_not_exists import ProjectsFromFiscalDoesNotExists


@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project_empresa'))
        db.session.execute(text('DELETE FROM project_fiscal'))
        db.session.execute(text('DELETE FROM refresh_token'))
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM user_project'))
        db.session.execute(text('DELETE FROM user'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.execute(text('DELETE FROM fiscal'))
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
    project_fiscal_repository = ProjectFiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )

        db.session.execute(
            insert_status_script,
            {
                'description': 'my_description',
                'created_at': datetime.now(timezone.utc)
            }
        )

        status = db.session.execute(
            text('''SELECT * FROM status WHERE description = :description '''),
            {
                'description': 'my_description'
            }
        ).fetchone()
        status_id = status.id

        db.session.execute(
            insert_project_script,
            {
                'status_id': status_id, 
                'verba_disponivel': 0, 
                'andamento_do_projeto': datetime.now(timezone.utc), 
                'start_date': datetime.now(timezone.utc), 
                'expected_completion_date': datetime.now(timezone.utc), 
                'end_date':datetime.now(timezone.utc)
            }
        )

        project = db.session.execute(
            text('''SELECT * FROM project WHERE status_id = :status_id '''),
            {
                'status_id': status_id
            }
        ).first()

        fiscal = db.session.execute(
            text('''SELECT * FROM fiscal WHERE name = :name '''),
            {
                'name': 'nome_teste'
            }
        ).first()

        db.session.commit()
    
    project_fiscal_repository.insert(
        project_id=project.id,
        fiscal_id=fiscal.id
    )

    project_fiscal = db.session.execute(
            text('''SELECT * FROM project_fiscal WHERE project_id = :project_id AND fiscal_id = :fiscal_id '''),
            {
                'project_id': project.id,
                'fiscal_id': fiscal.id
            }
        ).first()

    assert project_fiscal
    assert project_fiscal.project_id == project.id
    assert project_fiscal.fiscal_id == fiscal.id


    with pytest.raises(ProjectFiscalAlreadyExists):
        project_fiscal_repository.insert(
        project_id=project.id,
        fiscal_id=fiscal.id
        )

def test_find_all_from_fiscal(insert_project_script, insert_status_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_fiscal_repository = ProjectFiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir fiscal
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'Fiscal de Teste', 'created_at': datetime.now(timezone.utc)}
        )
        fiscal = db.session.execute(
            text('SELECT * FROM fiscal WHERE name = :name'),
            {'name': 'Fiscal de Teste'}
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

        # Relacionar projeto ao fiscal
        db.session.execute(
            text('INSERT INTO project_fiscal (project_id, fiscal_id, created_at) VALUES (:project_id, :fiscal_id, :created_at)'),
            {
                'project_id': project.id,
                'fiscal_id': fiscal.id,
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    # Testar busca
    results = project_fiscal_repository.find_all_from_fiscal(fiscal_id=fiscal.id)

    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0].fiscal_id == fiscal.id
    assert results[0].project_id == project.id

    # Testar exceção para fiscal sem projetos
    with pytest.raises(ProjectsFromFiscalDoesNotExists):
        project_fiscal_repository.find_all_from_fiscal(fiscal_id=9999)

def test_find(insert_project_script, insert_status_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_fiscal_repository = ProjectFiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir fiscal
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'Fiscal Teste Find', 'created_at': datetime.now(timezone.utc)}
        )
        fiscal = db.session.execute(
            text('SELECT * FROM fiscal WHERE name = :name'),
            {'name': 'Fiscal Teste Find'}
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

        # Relacionar projeto ao fiscal
        db.session.execute(
            text('INSERT INTO project_fiscal (project_id, fiscal_id, created_at) VALUES (:project_id, :fiscal_id, :created_at)'),
            {
                'project_id': project.id,
                'fiscal_id': fiscal.id,
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    # Teste de busca válida
    result = project_fiscal_repository.find(fiscal_id=fiscal.id, project_id=project.id)

    assert result.project_id == project.id
    assert result.fiscal_id == fiscal.id
    assert isinstance(result.created_at, datetime)

    # Teste de exceção ao buscar associação inexistente
    with pytest.raises(ProjectsFromFiscalDoesNotExists):
        project_fiscal_repository.find(fiscal_id=9999, project_id=9999)

def test_update_fiscal(insert_project_script, insert_status_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_fiscal_repository = ProjectFiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir dois fiscais
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'Fiscal Original', 'created_at': datetime.now(timezone.utc)}
        )
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'Fiscal Novo', 'created_at': datetime.now(timezone.utc)}
        )

        fiscal_original = db.session.execute(
            text('SELECT * FROM fiscal WHERE name = :name'),
            {'name': 'Fiscal Original'}
        ).fetchone()

        fiscal_novo = db.session.execute(
            text('SELECT * FROM fiscal WHERE name = :name'),
            {'name': 'Fiscal Novo'}
        ).fetchone()

        # Inserir status e projeto
        db.session.execute(
            insert_status_script,
            {'description': 'Status Update', 'created_at': datetime.now(timezone.utc)}
        )
        status = db.session.execute(
            text('SELECT * FROM status WHERE description = :description'),
            {'description': 'Status Update'}
        ).fetchone()

        db.session.execute(
            insert_project_script,
            {
                'status_id': status.id,
                'verba_disponivel': 3000,
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

        # Inserir relação original
        db.session.execute(
            text('INSERT INTO project_fiscal (project_id, fiscal_id, created_at) VALUES (:project_id, :fiscal_id, :created_at)'),
            {
                'project_id': project.id,
                'fiscal_id': fiscal_original.id,
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    # Atualizar para o novo fiscal
    project_fiscal_repository.update_fiscal(
        project_id=project.id,
        fiscal_id=fiscal_original.id,
        new_fiscal_id=fiscal_novo.id
    )

    with db_connection_handler as db:
        updated = db.session.execute(
            text('SELECT * FROM project_fiscal WHERE project_id = :project_id'),
            {'project_id': project.id}
        ).fetchone()

    assert updated.fiscal_id == fiscal_novo.id

def test_delete_project_fiscal_association(insert_project_script, insert_status_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    project_fiscal_repository = ProjectFiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        # Inserir fiscal
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {'name': 'Fiscal Delete', 'created_at': datetime.now(timezone.utc)}
        )
        fiscal = db.session.execute(
            text('SELECT * FROM fiscal WHERE name = :name'),
            {'name': 'Fiscal Delete'}
        ).fetchone()

        # Inserir status
        db.session.execute(
            insert_status_script,
            {'description': 'Status Delete', 'created_at': datetime.now(timezone.utc)}
        )
        status = db.session.execute(
            text('SELECT * FROM status WHERE description = :description'),
            {'description': 'Status Delete'}
        ).fetchone()

        # Inserir projeto
        db.session.execute(
            insert_project_script,
            {
                'status_id': status.id,
                'verba_disponivel': 4000,
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

        # Relacionar projeto ao fiscal
        db.session.execute(
            text('INSERT INTO project_fiscal (project_id, fiscal_id, created_at) VALUES (:project_id, :fiscal_id, :created_at)'),
            {
                'project_id': project.id,
                'fiscal_id': fiscal.id,
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    # Confirmar que o relacionamento existe
    with db_connection_handler as db:
        result = db.session.execute(
            text('SELECT * FROM project_fiscal WHERE project_id = :project_id AND fiscal_id = :fiscal_id'),
            {'project_id': project.id, 'fiscal_id': fiscal.id}
        ).fetchone()
        assert result is not None

    # Realizar a exclusão
    project_fiscal_repository.delete(project_id=project.id, fiscal_id=fiscal.id)

    # Verificar que foi deletado
    with db_connection_handler as db:
        result = db.session.execute(
            text('SELECT * FROM project_fiscal WHERE project_id = :project_id AND fiscal_id = :fiscal_id'),
            {'project_id': project.id, 'fiscal_id': fiscal.id}
        ).fetchone()
        assert result is None
