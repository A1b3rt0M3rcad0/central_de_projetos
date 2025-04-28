from src.infra.relational.repository.user_repository import UserRepository
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.password import Password
from src.security.value_objects.hashed_password import HashedPassword
from src.security.cryptography.blowfish_crypt import BlowfishCrypt
from src.security.cryptography.utils.salt import Salt
from src.domain.value_objects.email import Email
from src.domain.value_objects.roles import Role
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from sqlalchemy import text
from datetime import datetime, timezone
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

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM refresh_token'))
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM user_project'))
        db.session.execute(text('DELETE FROM user'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.commit()

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

def test_find_user(cpf, password, gen_salt, email, role) -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    user_repository = UserRepository(db_connection_handler)

    crypt = BlowfishCrypt()
    hashed_password = HashedPassword(password, crypt, gen_salt)
    salt = Salt(hashed_password.salt)
    now = datetime.now(timezone.utc)

    with db_connection_handler as db:
        insert_script = text('''
            INSERT INTO user (cpf, password, salt, role, email, created_at)
            VALUES (:cpf, :password, :salt, :role, :email, :created_at)
        ''')
        db.session.execute(insert_script, {
            'cpf': cpf.value,
            'password': hashed_password.hashed_password,
            'salt': salt.salt,
            'role': role.value,
            'email': email.email,
            'created_at': now
        })
        db.session.commit()

        result = user_repository.find(cpf=cpf)

        assert result.cpf.value == cpf.value
        assert result.email.email == email.email
        assert result.password == hashed_password.hashed_password
        assert result.role.value == role.value
        assert result.salt == salt.salt

def test_update_user(cpf, password, gen_salt, email, role) -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    user_repository = UserRepository(db_connection_handler)

    crypt = BlowfishCrypt()
    hashed_password = HashedPassword(password, crypt, gen_salt)
    salt = Salt(hashed_password.salt)
    now = datetime.now(timezone.utc)

    with db_connection_handler as db:
        insert_script = text('''
            INSERT INTO user (cpf, password, salt, role, email, created_at)
            VALUES (:cpf, :password, :salt, :role, :email, :created_at)
        ''')
        db.session.execute(insert_script, {
            'cpf': cpf.value,
            'password': hashed_password.hashed_password,
            'salt': salt.salt,
            'role': role.value,
            'email': email.email,
            'created_at': now
        })
        db.session.commit()

        update_params = {
            'role': Role('vereador').value
        }

        user_repository.update(cpf, update_params)

        finder = text('select * from user where cpf = :cpf')
        user_result = db.session.execute(finder, {'cpf':cpf.value}).fetchone()
        
        assert user_result.role == Role('vereador').value

def test_delete_user(cpf, password, gen_salt, email, role) -> None:

    db_connection_handler = DBConnectionHandler(StringConnection())
    user_repository = UserRepository(db_connection_handler)

    crypt = BlowfishCrypt()
    hashed_password = HashedPassword(password, crypt, gen_salt)
    salt = Salt(hashed_password.salt)
    now = datetime.now(timezone.utc)

    with db_connection_handler as db:
        insert_script = text('''
            INSERT INTO user (cpf, password, salt, role, email, created_at)
            VALUES (:cpf, :password, :salt, :role, :email, :created_at)
        ''')
        db.session.execute(insert_script, {
            'cpf': cpf.value,
            'password': hashed_password.hashed_password,
            'salt': salt.salt,
            'role': role.value,
            'email': email.email,
            'created_at': now
        })
        db.session.commit()

        user_repository.delete(cpf)

        finder = text('select * from user where cpf = :cpf')
        user_result = db.session.execute(finder, {'cpf':cpf.value}).fetchone()
        
        assert user_result is None