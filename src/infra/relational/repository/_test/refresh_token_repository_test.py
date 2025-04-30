from src.infra.relational.repository.refresh_token_repository import RefreshTokenRepository
from sqlalchemy import text
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from src.security.hashedpassword_factory import hashedpassword_factory
from src.domain.value_objects.password import Password
from src.security.value_objects.hashed_password import HashedPassword
from sqlalchemy import TextClause
from datetime import datetime, timezone
from src.domain.value_objects.cpf import CPF
from sqlalchemy import Row
from typing import Callable
import pytest

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project_type'))
        db.session.execute(text('DELETE FROM project_empresa'))
        db.session.execute(text('DELETE FROM refresh_token'))
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.execute(text('DELETE FROM user'))
        db.session.commit()

@pytest.fixture
def insert_user() -> TextClause:
    return text('INSERT INTO user (cpf, password, salt, role, email, created_at) VALUES (:cpf, :password, :salt, :role, :email, :created_at)')

@pytest.fixture
def find_refresh_token() -> TextClause:
    return text('SELECT * FROM refresh_token')

@pytest.fixture
def insert_refresh_token() -> TextClause:
    return text('INSERT INTO refresh_token (user_cpf, token) VALUES (:user_cpf, :token)')

@pytest.fixture
def hashedpassword() -> HashedPassword:
    return hashedpassword_factory(Password('Senha@123'))

@pytest.fixture
def database() -> DBConnectionHandler:
    return DBConnectionHandler(StringConnection())

@pytest.fixture
def insert_user_execute(insert_user, hashedpassword, database) -> callable:
    def executor() -> None:
        with database as db:
            db.session.execute(
                insert_user,
                {
                    'cpf': '16290598031',
                    'password': hashedpassword.hashed_password,
                    'salt': hashedpassword.salt,
                    'role': 'ADMIN',
                    'email': 'example@example.com',
                    'created_at': datetime.now(timezone.utc)
                }
            )
            db.session.commit()
    return executor

@pytest.fixture
def find_refresh_token_execute(find_refresh_token, database) -> Callable[[None], Row]:
    def executor() -> Row:
        with database as db:
            result = db.session.execute(
                find_refresh_token
            )
        return result.fetchone()
    return executor

@pytest.fixture
def insert_refresh_token_execute(insert_refresh_token, database) -> Callable[[None], None]:
    def executor() -> None:
        with database as db:
            db.session.execute(
                insert_refresh_token,
                {
                    'user_cpf': '16290598031',
                    'token': 'asd12easd'
                }
            )
            db.session.commit()
    return executor

def test_insert_refresh_token(insert_user_execute, database, find_refresh_token_execute) -> None:

    insert_user_execute()

    refresh_token_repository = RefreshTokenRepository(database)
    refresh_token_repository.insert(
        user_cpf=CPF('16290598031'),
        token='asd12easd'
    )

    result = find_refresh_token_execute()

    assert result is not None
    assert result.user_cpf == '16290598031'
    assert result.token is not None

def test_find_refresh_token(insert_refresh_token_execute, insert_user_execute, database) -> None:
    insert_user_execute()
    insert_refresh_token_execute()

    refresh_token = RefreshTokenRepository(database)
    entity = refresh_token.find(
        user_cpf=CPF('16290598031')
    )

    assert entity is not None
    assert entity.cpf == '16290598031'
    assert entity.token == 'asd12easd'

def test_update_refresh_token(insert_refresh_token_execute, insert_user_execute, find_refresh_token_execute, database) -> None:
    insert_user_execute()
    insert_refresh_token_execute()

    refresh_token = RefreshTokenRepository(database)
    refresh_token.update(
        user_cpf=CPF('16290598031'),
        new_token='asd12easd123'
    )

    refresh_token = find_refresh_token_execute()

    assert refresh_token is not None
    assert refresh_token.token == 'asd12easd123'
    assert refresh_token.user_cpf == '16290598031'