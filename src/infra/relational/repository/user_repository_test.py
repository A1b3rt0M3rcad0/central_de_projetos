#pylint:disable=all
from src.infra.relational.repository.user_repository import UserRepository
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.password import Password
from src.security.value_objects.hashed_password import HashedPassword
from src.security.cryptography.blowfish_crypt import BlowfishCrypt
from src.security.cryptography.utils.salt import Salt
from src.domain.value_objects.email import Email
from src.domain.value_objects.roles import Role
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
from sqlalchemy import text
from src.infra.relational.models.user import User
import pytest

@pytest.fixture
def cpf() -> CPF:
    return CPF('874.698.600-61')

@pytest.fixture
def password() -> Password:
    return Password('Password@123')

@pytest.fixture
def gen_salt() -> Salt:
    return Salt()

@pytest.fixture
def email() -> Email:
    return Email('example@email.com')

@pytest.fixture
def role() -> Role:
    return Role('admin')


def test_insert_user(cpf, password, gen_salt, email, role) -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    user_repository = UserRepository(db_connection_handler)

    crypt = BlowfishCrypt()
    hashed_password = HashedPassword(password, crypt, gen_salt)
    salt = Salt(hashed_password.salt)

    user_repository.insert(cpf, hashed_password, salt, role, email)

    with db_connection_handler as db:

        finder = text('select * from user where cpf = :cpf')
        user_result = db.session.execute(finder, {'cpf':cpf.value}).fetchone()
        assert user_result.cpf == cpf.value
        assert HashedPassword(user_result.password, crypt, Salt(user_result.salt)).check(password)
        assert user_result.salt == gen_salt.salt
        assert user_result.email == email.email
        assert user_result.role == role.value


        deleter = text("delete from user where cpf = :cpf;")
        db.session.execute(deleter, {'cpf':cpf.value})

        db.session.commit()