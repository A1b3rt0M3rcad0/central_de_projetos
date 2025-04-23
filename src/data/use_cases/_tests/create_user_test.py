#pylint:disable=all
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.roles import Role
from src.data.use_cases.create_user import CreateUser
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.repository.user_repository import UserRepository
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from src.errors.use_cases.create_user_error import CreateUserError
from src.infra.relational.models.user import User
from sqlalchemy import text
import pytest

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.execute(text('DELETE FROM user'))
        db.session.commit()

@pytest.fixture
def db_connection_handler() -> DBConnectionHandler:
    return DBConnectionHandler(StringConnection())

@pytest.fixture
def create_user_case(db_connection_handler) -> CreateUser:
    return CreateUser(UserRepository(db_connection_handler))

def test_create_user(db_connection_handler, create_user_case) -> None:
    create_user_case.create(
        cpf=CPF('081.885.610-61'),
        email=Email('josemaria@example.com'),
        role=Role('ADMIN'),
        password=Password('Password@123'),
    )
    find_user_script = text('SELECT * FROM user')

    with db_connection_handler as db:
        result = db.session.execute(find_user_script).fetchone()
        assert result.cpf == '08188561061'
        assert result.email == 'josemaria@example.com'
        assert result.role == 'ADMIN'
        assert result.password
        assert result.salt

    with pytest.raises(CreateUserError):
        create_user_case.create(
            cpf=CPF('081.885.610-61'),
            email=Email('josemaria@example.com'),
            role=Role('ADMIN'),
            password=Password('Password@123'),
        )
        assert False, 'Exception não levantanda'