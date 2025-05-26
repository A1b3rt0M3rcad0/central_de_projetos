from src.infra.relational.repository.project_type_repository import ProjectTypeRepository
from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
import pytest
from src.infra.relational.models.project import Project
from src.infra.relational.models.status import Status
from src.infra.relational.models.types import Types
from sqlalchemy import text
from sqlalchemy import TextClause
from src.errors.repository.not_exists_error.project_type_not_exists import ProjectTypeNotExists

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project_type'))
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

@pytest.fixture
def insert_type_script() -> TextClause:
    return text('INSERT INTO types (name, created_at) VALUES (:name, :created_at)')

@pytest.fixture
def project_type_repo() -> ProjectTypeRepository:
    return ProjectTypeRepository(DBConnectionHandler(StringConnection()))

def test_insert_project_type(project_type_repo, insert_project_script, insert_status_script, insert_type_script):
    with DBConnectionHandler(StringConnection()) as db:
        # Inserindo um status
        db.session.execute(insert_status_script, {'description': 'Active', 'created_at': '2025-04-01'})
        db.session.commit()

        # Buscando o ID do status inserido
        status_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        # Inserindo um tipo
        db.session.execute(insert_type_script, {'name': 'Development', 'created_at': '2025-04-01'})
        db.session.commit()

        # Buscando o ID do tipo inserido
        type_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        # Inserindo um projeto
        db.session.execute(insert_project_script, {'status_id': status_id, 'verba_disponivel': 1000, 
                                                   'andamento_do_projeto': 'Ongoing', 'start_date': '2025-04-01', 
                                                   'expected_completion_date': '2025-12-31', 'end_date': '2026-12-31'})
        db.session.commit()

        # Buscando o ID do projeto inserido
        project_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        # Inserindo a relação project_type
        project_type_repo.insert(project_id, type_id)

        # Buscando a relação inserida
        result = db.session.query(ProjectType).filter_by(project_id=project_id, type_id=type_id).first()
        assert result is not None
        assert result.project_id == project_id
        assert result.type_id == type_id

def test_find_project_type(project_type_repo, insert_project_script, insert_status_script, insert_type_script):
    with DBConnectionHandler(StringConnection()) as db:
        # Inserindo status, tipo e projeto
        db.session.execute(insert_status_script, {'description': 'Active', 'created_at': '2025-04-01'})
        db.session.commit()

        # Buscando o ID do status inserido
        status_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        db.session.execute(insert_type_script, {'name': 'Excluid', 'created_at': '2025-04-01'})
        db.session.commit()

        # Buscando o ID do tipo inserido
        type_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        db.session.execute(insert_project_script, {'status_id': status_id, 'verba_disponivel': 1000, 
                                                   'andamento_do_projeto': 'Ongoing', 'start_date': '2025-04-01', 
                                                   'expected_completion_date': '2025-12-31', 'end_date': '2026-12-31'})
        db.session.commit()

        # Buscando o ID do projeto inserido
        project_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        # Inserindo a relação project_type
        project_type_repo.insert(project_id, type_id)

        # Testando o método find
        result = project_type_repo.find(project_id, type_id)

        assert result is not None
        assert result.project_id == project_id
        assert result.type_id == type_id
        assert result.created_at is not None

def test_find_all_from_type(project_type_repo, insert_project_script, insert_status_script, insert_type_script):
    with DBConnectionHandler(StringConnection()) as db:
        # Inserindo status, tipo e projeto
        db.session.execute(insert_status_script, {'description': 'Active', 'created_at': '2025-04-01'})
        db.session.commit()

        # Buscando o ID do status inserido
        status_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        db.session.execute(insert_type_script, {'name': 'Excludment', 'created_at': '2025-04-01'})
        db.session.commit()

        # Buscando o ID do tipo inserido
        type_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        db.session.execute(insert_project_script, {'status_id': status_id, 'verba_disponivel': 1000, 
                                                   'andamento_do_projeto': 'Ongoing', 'start_date': '2025-04-01', 
                                                   'expected_completion_date': '2025-12-31', 'end_date': '2026-12-31'})
        db.session.commit()

        # Buscando o ID do projeto inserido
        project_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        # Inserindo outro projeto com o mesmo tipo
        db.session.execute(insert_project_script, {'status_id': status_id, 'verba_disponivel': 2000, 
                                                   'andamento_do_projeto': 'Completed', 'start_date': '2025-03-01', 
                                                   'expected_completion_date': '2025-09-30', 'end_date': '2025-10-31'})
        db.session.commit()

        # Buscando o ID do segundo projeto inserido
        project_id_2 = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        # Inserindo a relação project_type para ambos os projetos
        project_type_repo.insert(project_id, type_id)
        project_type_repo.insert(project_id_2, type_id)

        # Testando o método find_all_from_type
        result = project_type_repo.find_all_from_type(type_id)

        # Verificando se a lista retornada contém dois itens
        assert len(result) == 2

        # Verificando se os projetos retornados têm os tipos e ids corretos
        assert all(item.type_id == type_id for item in result)
        assert all(item.project_id in [project_id, project_id_2] for item in result)
        assert all(item.created_at is not None for item in result)

def test_update_type(project_type_repo, insert_project_script, insert_status_script, insert_type_script):
    with DBConnectionHandler(StringConnection()) as db:
        # Inserindo status, tipo e projeto
        db.session.execute(insert_status_script, {'description': 'Active', 'created_at': '2025-04-01'})
        db.session.commit()

        # Buscando o ID do status inserido
        status_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        db.session.execute(insert_type_script, {'name': 'Developments', 'created_at': '2025-04-01'})
        db.session.commit()

        # Buscando o ID do tipo inserido
        type_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        db.session.execute(insert_project_script, {'status_id': status_id, 'verba_disponivel': 1000, 
                                                   'andamento_do_projeto': 'Ongoing', 'start_date': '2025-04-01', 
                                                   'expected_completion_date': '2025-12-31', 'end_date': '2026-12-31'})
        db.session.commit()

        # Buscando o ID do projeto inserido
        project_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        # Inserindo a relação project_type
        project_type_repo.insert(project_id, type_id)

        # Inserindo um novo tipo para atualizar
        db.session.execute(insert_type_script, {'name': 'Testing', 'created_at': '2025-04-01'})
        db.session.commit()

        # Buscando o ID do novo tipo inserido
        new_type_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()

        # Chamando o método para atualizar o tipo
        project_type_repo.update_type(project_id, type_id, new_type_id)

        # Verificando se a relação foi atualizada corretamente
        updated_relation = db.session.query(ProjectType).filter_by(project_id=project_id).first()
        assert updated_relation is not None
        assert updated_relation.type_id == new_type_id

        # Verificando se o tipo antigo foi alterado
        old_relation = db.session.query(ProjectType).filter_by(project_id=project_id, type_id=type_id).first()
        assert old_relation is None  # A relação antiga não deve existir mais

def test_delete_project_type(project_type_repo, insert_project_script, insert_status_script, insert_type_script):
    with DBConnectionHandler(StringConnection()) as db:
        # Inserindo dados iniciais
        db.session.execute(insert_status_script, {'description': 'Active', 'created_at': '2025-04-01'})
        db.session.execute(insert_type_script, {'name': 'Research', 'created_at': '2025-04-01'})
        db.session.commit()

        status = db.session.query(Status).filter_by(description='Active').first()
        tipo = db.session.query(Types).filter_by(name='Research').first()

        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'verba_disponivel': 1000,
            'andamento_do_projeto': 'Ongoing',
            'start_date': '2025-04-01',
            'expected_completion_date': '2025-12-31',
            'end_date': '2026-12-31'
        })
        db.session.commit()

        project = db.session.query(Project).first()

    # Inserindo a relação
    project_type_repo.insert(project.id, tipo.id)

    # Verificando a relação
    relation = project_type_repo.find(project.id, tipo.id)

    assert relation is not None

    project_type_repo.delete(project.id, tipo.id)


    # Verificando a relação
    with pytest.raises(ProjectTypeNotExists):
        relation = project_type_repo.find(project.id, tipo.id)