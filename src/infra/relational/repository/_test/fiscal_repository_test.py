from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
import pytest
from sqlalchemy import text
from datetime import datetime, timezone

from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.security.hashedpassword_factory import hashedpassword_factory

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
from src.infra.relational.models.project_folder import ProjectFolder
from src.infra.relational.models.folder import Folder
# pylint: enable=unused-import

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project_type'))
        db.session.execute(text('DELETE FROM project_empresa'))
        db.session.execute(text('DELETE FROM fiscal'))
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.commit()

def test_insert_fiscal() -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    fiscal_repository.insert(name='nome_teste')

    with db_connection_handler as db:
        result = db.session.execute(
            text('SELECT * FROM fiscal')
        ).fetchone()
    
    assert result is not None
    assert result.name == 'nome_teste'

def test_find_by_name() -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()
    
    fiscal = fiscal_repository.find_by_name('nome_teste')

    assert fiscal
    assert fiscal.name == 'nome_teste'

def test_update() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    fiscal_repository.update('nome_teste', 'new_nome_teste')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM fiscal')).fetchone()

    assert result
    assert result.name == 'new_nome_teste'

def test_delete() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        db.session.commit()

    fiscal_repository.delete('nome_teste')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM fiscal')).fetchone()
    
    assert not result

def test_find_by_id() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    now = datetime.now(timezone.utc)

    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': now
            }
        )
        fiscal_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()
        db.session.commit()

    fiscal = fiscal_repository.find_by_id(fiscal_id)

    assert fiscal
    assert fiscal.fiscal_id == fiscal_id
    assert fiscal.name == 'nome_teste'

def test_insert_all_from_fiscal() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    email = Email(email='teste@email.com')
    password = hashedpassword_factory(Password(password='Senha@123'))
    phone = '48999990000'

    fiscal_repository.insert_all_from_fiscal(
        name='nome_teste',
        email=email,
        password=password,
        phone=phone
    )

    with db_connection_handler as db:
        result = db.session.execute(
            text('SELECT * FROM fiscal WHERE name = :name'),
            {'name': 'nome_teste'}
        ).fetchone()

    assert result is not None
    assert result.name == 'nome_teste'
    assert result.email == 'teste@email.com'
    assert result.phone == '48999990000'
    assert result.password == password.hashed_password

def test_insert_refresh_token() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    # First create a fiscal
    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        fiscal_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()
        db.session.commit()

    # Then insert refresh token
    fiscal_repository.insert_refresh_token(fiscal_id=fiscal_id, refresh_token='refresh_token_teste')

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM fiscal WHERE id = :id'), {'id': fiscal_id}).fetchone()
    
    assert result is not None
    assert result.refresh_token == 'refresh_token_teste'

def test_update_email() -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    fiscal_repository = FiscalRepository(db_connection_handler)

    # First create a fiscal
    with db_connection_handler as db:
        db.session.execute(
            text('INSERT INTO fiscal (name, created_at) VALUES (:name, :created_at)'),
            {
                'name': 'nome_teste',
                'created_at': datetime.now(timezone.utc)
            }
        )
        fiscal_id = db.session.execute(text('SELECT LAST_INSERT_ID()')).scalar()
        db.session.commit()

    # Then update email (método aceita name, não fiscal_id)
    fiscal_repository.update_email(name='nome_teste', email=Email(email='teste@email.com'))

    with db_connection_handler as db:
        result = db.session.execute(text('SELECT * FROM fiscal WHERE id = :id'), {'id': fiscal_id}).fetchone()
    
    assert result is not None
    assert result.email == 'teste@email.com'