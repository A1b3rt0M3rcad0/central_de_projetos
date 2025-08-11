from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
import pytest
from sqlalchemy import text
from datetime import datetime, timezone

# Import models to ensure SQLAlchemy can resolve relationships
# These imports are necessary for SQLAlchemy to properly configure relationships
# pylint: disable=unused-import
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.models.project import Project
from src.infra.relational.models.history_project import HistoryProject
from src.infra.relational.models.project_bairro import ProjectBairro
from src.infra.relational.models.project_empresa import ProjectEmpresa
from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.models.user_project import UserProject
from src.infra.relational.models.bairro import Bairro
from src.infra.relational.models.empresa import Empresa
from src.infra.relational.models.types import Types
from src.infra.relational.models.user import User
from src.infra.relational.models.status import Status
from src.infra.relational.models.refresh_token import RefreshToken
from src.infra.relational.models.work_project import WorkProject
# pylint: enable=unused-import

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM work_projects'))
        db.session.execute(text('DELETE FROM project_type'))
        db.session.execute(text('DELETE FROM project_empresa'))
        db.session.execute(text('DELETE FROM project_fiscal'))
        db.session.execute(text('DELETE FROM project_bairro'))
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM fiscal'))
        db.session.execute(text('DELETE FROM status'))
        db.session.commit()

@pytest.fixture
def datetime_fixture() -> datetime:
    return datetime.now(timezone.utc)

@pytest.fixture
def insert_status_script() -> text:
    return text('''INSERT INTO status (description, created_at) VALUES (:description, :created_at)''')

@pytest.fixture
def insert_project_script() -> text:
    return text('''
    insert into project (status_id, name, verba_disponivel, andamento_do_projeto, start_date, expected_completion_date, end_date) 
    VALUES (:status_id, :name, :verba_disponivel, :andamento_do_projeto, :start_date, :expected_completion_date, :end_date)
    ''')

@pytest.fixture
def insert_fiscal_script() -> text:
    return text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)')

@pytest.fixture
def insert_work_projects_script() -> text:
    return text('''
    insert into work_projects (project_id, fiscal_id, title, description, photo_name, created_at, updated_at) 
    VALUES (:project_id, :fiscal_id, :title, :description, :photo_name, :created_at, :updated_at)
    ''')

def test_insert_work_projects(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Testar inserção do work_projects
        work_projects_repository.insert(
            project_id=project.id,
            fiscal_id=fiscal.id,
            title='Trabalho Teste',
            description='Descrição do trabalho teste',
            photo_name='foto_teste.jpg'
        )
        
        # Verificar se foi inserido
        result = db.session.execute(text('SELECT * FROM work_projects')).first()
        
        assert result is not None
        assert result.project_id == project.id
        assert result.fiscal_id == fiscal.id
        assert result.title == 'Trabalho Teste'
        assert result.description == 'Descrição do trabalho teste'
        assert result.photo_name == 'foto_teste.jpg'

def test_find_work_projects(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projects
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Teste',
            'description': 'Descrição do trabalho teste',
            'photo_name': 'foto_teste.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.commit()
        work_projects_db = db.session.execute(text('SELECT * FROM work_projects')).first()
        
        # Testar busca
        work_projects = work_projects_repository.find(work_projects_db.id)
        
        assert work_projects is not None
        assert work_projects.id == work_projects_db.id
        assert work_projects.title == 'Trabalho Teste'
        assert work_projects.description == 'Descrição do trabalho teste'
        assert work_projects.photo_name == 'foto_teste.jpg'
        assert work_projects.project_id == project.id
        assert work_projects.fiscal_id == fiscal.id
        assert work_projects.fiscal.name == 'Fiscal Teste'
        assert work_projects.project.name == 'Projeto Teste'

def test_find_all_work_projectss(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projectss
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Teste 1',
            'description': 'Descrição do trabalho teste 1',
            'photo_name': 'foto_teste1.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Teste 2',
            'description': 'Descrição do trabalho teste 2',
            'photo_name': 'foto_teste2.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.commit()
        
        # Testar busca de todos
        work_projectss = work_projects_repository.find_all()
        
        assert len(work_projectss) == 2
        assert work_projectss[0].title == 'Trabalho Teste 1'
        assert work_projectss[1].title == 'Trabalho Teste 2'

def test_find_by_project(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projetos
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste 1',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste 2',
            'verba_disponivel': 20000.0,
            'andamento_do_projeto': 'Fase final',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        projects = db.session.execute(text('SELECT * FROM project')).fetchall()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projectss para diferentes projetos
        db.session.execute(insert_work_projects_script, {
            'project_id': projects[0].id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Projeto 1',
            'description': 'Descrição do trabalho projeto 1',
            'photo_name': 'foto_projeto1.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.execute(insert_work_projects_script, {
            'project_id': projects[1].id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Projeto 2',
            'description': 'Descrição do trabalho projeto 2',
            'photo_name': 'foto_projeto2.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.commit()
        
        # Testar busca por projeto
        work_projectss = work_projects_repository.find_by_project(projects[0].id)
        
        assert len(work_projectss) == 1
        assert work_projectss[0].title == 'Trabalho Projeto 1'
        assert work_projectss[0].project_id == projects[0].id

def test_find_by_fiscal(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscais
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste 1',
            'created_at': datetime_fixture
        })
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste 2',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscals = db.session.execute(text('SELECT * FROM fiscal')).fetchall()
        
        # Inserir work_projectss para diferentes fiscais
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscals[0].id,
            'title': 'Trabalho Fiscal 1',
            'description': 'Descrição do trabalho fiscal 1',
            'photo_name': 'foto_fiscal1.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscals[1].id,
            'title': 'Trabalho Fiscal 2',
            'description': 'Descrição do trabalho fiscal 2',
            'photo_name': 'foto_fiscal2.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.commit()
        
        # Testar busca por fiscal
        work_projectss = work_projects_repository.find_by_fiscal(fiscals[0].id)
        
        assert len(work_projectss) == 1
        assert work_projectss[0].title == 'Trabalho Fiscal 1'
        assert work_projectss[0].fiscal_id == fiscals[0].id

def test_find_by_project_and_fiscal(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projetos
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste 1',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste 2',
            'verba_disponivel': 20000.0,
            'andamento_do_projeto': 'Fase final',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        projects = db.session.execute(text('SELECT * FROM project')).fetchall()
        
        # Inserir fiscais
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste 1',
            'created_at': datetime_fixture
        })
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste 2',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscals = db.session.execute(text('SELECT * FROM fiscal')).fetchall()
        
        # Inserir work_projectss
        db.session.execute(insert_work_projects_script, {
            'project_id': projects[0].id,
            'fiscal_id': fiscals[0].id,
            'title': 'Trabalho Projeto1 Fiscal1',
            'description': 'Descrição do trabalho projeto1 fiscal1',
            'photo_name': 'foto_projeto1_fiscal1.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.execute(insert_work_projects_script, {
            'project_id': projects[0].id,
            'fiscal_id': fiscals[1].id,
            'title': 'Trabalho Projeto1 Fiscal2',
            'description': 'Descrição do trabalho projeto1 fiscal2',
            'photo_name': 'foto_projeto1_fiscal2.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.commit()
        
        # Testar busca por projeto e fiscal
        work_projectss = work_projects_repository.find_by_project_and_fiscal(projects[0].id, fiscals[0].id)
        
        assert len(work_projectss) == 1
        assert work_projectss[0].title == 'Trabalho Projeto1 Fiscal1'
        assert work_projectss[0].project_id == projects[0].id
        assert work_projectss[0].fiscal_id == fiscals[0].id

def test_find_by_title(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projects
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Específico',
            'description': 'Descrição do trabalho específico',
            'photo_name': 'foto_especifica.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.commit()
        
        # Testar busca por título
        work_projects = work_projects_repository.find_by_title('Trabalho Específico')
        
        assert work_projects is not None
        assert work_projects.title == 'Trabalho Específico'
        assert work_projects.description == 'Descrição do trabalho específico'
        assert work_projects.photo_name == 'foto_especifica.jpg'

def test_count_work_projects(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projectss
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Teste 1',
            'description': 'Descrição do trabalho teste 1',
            'photo_name': 'foto_teste1.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Teste 2',
            'description': 'Descrição do trabalho teste 2',
            'photo_name': 'foto_teste2.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Teste 3',
            'description': 'Descrição do trabalho teste 3',
            'photo_name': 'foto_teste3.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.commit()
        
        # Testar contagem
        count_result = work_projects_repository.count_work_projects()
        
        assert count_result['total'] == 3

def test_get_work_projects_with_pagination(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projectss
        for i in range(5):
            db.session.execute(insert_work_projects_script, {
                'project_id': project.id,
                'fiscal_id': fiscal.id,
                'title': f'Trabalho Teste {i+1}',
                'description': f'Descrição do trabalho teste {i+1}',
                'photo_name': f'foto_teste{i+1}.jpg',
                'created_at': datetime_fixture,
                'updated_at': datetime_fixture
            })
        db.session.commit()
        
        # Testar paginação
        result = work_projects_repository.get_work_projects_with_pagination(page=1, page_size=2)
        
        assert result['total'] == 5
        assert len(result['data']) == 2
        assert result['data'][0].title == 'Trabalho Teste 1'
        assert result['data'][1].title == 'Trabalho Teste 2'

def test_get_work_projects_with_pagination_by_fiscal(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    """Testa a paginação de work projects por fiscal"""
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projects para o fiscal
        for i in range(3):
            db.session.execute(insert_work_projects_script, {
                'project_id': project.id,
                'fiscal_id': fiscal.id,
                'title': f'Trabalho Fiscal {i+1}',
                'description': f'Descrição do trabalho fiscal {i+1}',
                'photo_name': f'foto_fiscal{i+1}.jpg',
                'created_at': datetime_fixture,
                'updated_at': datetime_fixture
            })
        db.session.commit()
        
        # Testar paginação por fiscal
        result = work_projects_repository.get_work_projects_with_pagination_by_fiscal(
            fiscal_id=fiscal.id, 
            page=1, 
            page_size=2
        )
        
        assert result['total'] == 3
        assert len(result['data']) == 2
        assert result['data'][0].fiscal_id == fiscal.id
        assert result['data'][1].fiscal_id == fiscal.id

def test_get_work_projects_with_pagination_by_fiscal_and_project(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    """Testa a paginação de work projects por fiscal e projeto"""
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projects para o fiscal e projeto
        for i in range(2):
            db.session.execute(insert_work_projects_script, {
                'project_id': project.id,
                'fiscal_id': fiscal.id,
                'title': f'Trabalho Fiscal Projeto {i+1}',
                'description': f'Descrição do trabalho fiscal projeto {i+1}',
                'photo_name': f'foto_fiscal_projeto{i+1}.jpg',
                'created_at': datetime_fixture,
                'updated_at': datetime_fixture
            })
        db.session.commit()
        
        # Testar paginação por fiscal e projeto
        result = work_projects_repository.get_work_projects_with_pagination_by_fiscal_and_project(
            fiscal_id=fiscal.id,
            project_id=project.id,
            page=1, 
            page_size=2
        )
        
        assert result['total'] == 2
        assert len(result['data']) == 2
        assert result['data'][0].fiscal_id == fiscal.id
        assert result['data'][0].project_id == project.id
        assert result['data'][1].fiscal_id == fiscal.id
        assert result['data'][1].project_id == project.id

def test_update_work_projects(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projects
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho Original',
            'description': 'Descrição original',
            'photo_name': 'foto_original.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.commit()
        work_projects_db = db.session.execute(text('SELECT * FROM work_projects')).first()
        
        # Testar atualização
        work_projects_repository.update(work_projects_db.id, {
            'title': 'Trabalho Atualizado',
            'description': 'Descrição atualizada',
            'photo_name': 'foto_atualizada.jpg'
        })
        
        # Verificar se foi atualizado
        updated_work_projects = work_projects_repository.find(work_projects_db.id)
        
        assert updated_work_projects.title == 'Trabalho Atualizado'
        assert updated_work_projects.description == 'Descrição atualizada'
        assert updated_work_projects.photo_name == 'foto_atualizada.jpg'

def test_delete_work_projects(datetime_fixture, insert_status_script, insert_project_script, insert_fiscal_script, insert_work_projects_script) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    work_projects_repository = WorkProjectRepository(db_connection_handler)
    
    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Em andamento',
            'created_at': datetime_fixture
        })
        db.session.commit()
        status = db.session.execute(text('SELECT * FROM status')).first()
        
        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status.id,
            'name': 'Projeto Teste',
            'verba_disponivel': 10000.0,
            'andamento_do_projeto': 'Fase inicial',
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': None
        })
        db.session.commit()
        project = db.session.execute(text('SELECT * FROM project')).first()
        
        # Inserir fiscal
        db.session.execute(insert_fiscal_script, {
            'name': 'Fiscal Teste',
            'created_at': datetime_fixture
        })
        db.session.commit()
        fiscal = db.session.execute(text('SELECT * FROM fiscal')).first()
        
        # Inserir work_projects
        db.session.execute(insert_work_projects_script, {
            'project_id': project.id,
            'fiscal_id': fiscal.id,
            'title': 'Trabalho para Deletar',
            'description': 'Descrição do trabalho para deletar',
            'photo_name': 'foto_deletar.jpg',
            'created_at': datetime_fixture,
            'updated_at': datetime_fixture
        })
        db.session.commit()
        work_projects_db = db.session.execute(text('SELECT * FROM work_projects')).first()
        
        # Verificar se existe antes de deletar
        assert work_projects_db is not None
        
        # Testar deleção
        work_projects_repository.delete(work_projects_db.id)
        
        # Verificar se foi deletado
        result = db.session.execute(text('SELECT * FROM work_projects')).first()
        assert result is None 