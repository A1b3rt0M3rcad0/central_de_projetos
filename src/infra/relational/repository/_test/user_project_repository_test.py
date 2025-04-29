from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.t_string_connection import TStringConnection as StringConnection
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime, timezone
from sqlalchemy import text, TextClause
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.roles import Role
from src.security.cryptography.utils.salt import Salt
from src.security.value_objects.hashed_password import HashedPassword
from src.security.cryptography.blowfish_crypt import BlowfishCrypt
from src.infra.relational.repository.user_project_repository import UserProjectRepository
import pytest

@pytest.fixture
def monetary_value() -> MonetaryValue:
    '''
    MonetaryValue:
        property:
            -> value -> Decimal
    '''
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

@pytest.fixture
def insert_user_project() -> TextClause:
    return text('''
    INSERT INTO user_project (user_cpf, project_id, assignment_date) VALUES (:user_cpf, :project_id, :assignment_date)
    ''')

@pytest.fixture()
def select_user_project() -> TextClause:
    return text('''SELECT * FROM user_project WHERE user_cpf = :user_cpf AND project_id= :project_id''')

@pytest.fixture
def insert_user() -> TextClause:
    return text('INSERT INTO user (cpf, password, salt, role, email, created_at) VALUES (:cpf, :password, :salt, :role, :email, :created_at)')

@pytest.fixture
def cpf() -> CPF:
    '''
    CPF:
        property:
            -> value -> str
    '''
    return CPF('874.698.600-61')

@pytest.fixture
def password() -> HashedPassword:
    '''
    HashedPassword:
        property:
            -> hashed_password -> bytes
            -> salt -> bytes
    '''
    password = Password('Password@123')
    salt = Salt()
    crypt = BlowfishCrypt()
    hashed_password = HashedPassword(password, crypt, salt)
    return hashed_password

@pytest.fixture
def email() -> Email:
    '''
    Email:
        property:
            -> email -> str
    '''
    return Email('example@email.com')

@pytest.fixture
def role() -> Role:
    '''
    Role:
        property:
            -> value -> str
    '''
    return Role('admin')

@pytest.fixture(autouse=True)
def cleanup_all():
    db_connection_handler = DBConnectionHandler(StringConnection())
    with db_connection_handler as db:
        db.session.execute(text('DELETE FROM project_empresa'))
        db.session.execute(text('DELETE FROM refresh_token'))
        db.session.execute(text('DELETE FROM history_project'))
        db.session.execute(text('DELETE FROM user_project'))
        db.session.execute(text('DELETE FROM user'))
        db.session.execute(text('DELETE FROM project'))
        db.session.execute(text('DELETE FROM status'))
        db.session.commit()

def test_insert(
    insert_status_script,
    select_status_script,
    monetary_value,
    andamento_do_projeto,
    datetime_fixture,
    insert_project_script,
    select_project_script,
    insert_user,
    cpf,
    password,
    email,
    role,
    select_user_project
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())

    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Ativo',
            'created_at': datetime_fixture
        })
        status_result = db.session.execute(select_status_script).fetchone()
        status_id = status_result.id

        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status_id,
            'verba_disponivel': monetary_value.value,
            'andamento_do_projeto': andamento_do_projeto,
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': datetime_fixture,
        })
        project_result = db.session.execute(select_project_script, {
            'status_id': status_id
        }).fetchone()
        project_id = project_result.id

        # Inserir usuário
        db.session.execute(insert_user, {
            'cpf': cpf.value,
            'password': password.hashed_password,
            'salt': password.salt,
            'role': role.value,
            'email': email.email,
            'created_at': datetime_fixture,
        })
        db.session.commit()

    # Testar inserção no user_project
    repo = UserProjectRepository(db_connection_handler)
    repo.insert(cpf, project_id)

    with db_connection_handler as db:
        result = db.session.execute(select_user_project, {
            'user_cpf': cpf.value,
            'project_id': project_id
        }).fetchone()
        assert result is not None
        assert result.user_cpf == cpf.value
        assert result.project_id == project_id

def test_find(
    insert_status_script,
    select_status_script,
    monetary_value,
    andamento_do_projeto,
    datetime_fixture,
    insert_project_script,
    select_project_script,
    insert_user,
    cpf,
    password,
    email,
    role,
    insert_user_project
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())

    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Ativo',
            'created_at': datetime_fixture
        })
        status_result = db.session.execute(select_status_script).fetchone()
        status_id = status_result.id

        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status_id,
            'verba_disponivel': monetary_value.value,
            'andamento_do_projeto': andamento_do_projeto,
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': datetime_fixture,
        })
        project_result = db.session.execute(select_project_script, {
            'status_id': status_id
        }).fetchone()
        project_id = project_result.id

        # Inserir usuário
        db.session.execute(insert_user, {
            'cpf': cpf.value,
            'password': password.hashed_password,
            'salt': password.salt,
            'role': role.value,
            'email': email.email,
            'created_at': datetime_fixture,
        })

        # Inserir user_project manualmente
        db.session.execute(insert_user_project, {
            'user_cpf': cpf.value,
            'project_id': project_id,
            'assignment_date': datetime_fixture
        })
        db.session.commit()

    # Testar método find
    repo = UserProjectRepository(db_connection_handler)
    user_project_entity = repo.find(cpf, project_id)

    assert user_project_entity is not None
    assert user_project_entity.cpf == cpf.value
    assert user_project_entity.project_id == project_id

def test_find_all(
    insert_status_script,
    select_status_script,
    monetary_value,
    andamento_do_projeto,
    datetime_fixture,
    insert_project_script,
    select_project_script,
    insert_user,
    cpf,
    password,
    email,
    role,
    insert_user_project
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())

    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Ativo',
            'created_at': datetime_fixture
        })
        status_result = db.session.execute(select_status_script).fetchone()
        status_id = status_result.id

        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status_id,
            'verba_disponivel': monetary_value.value,
            'andamento_do_projeto': andamento_do_projeto,
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': datetime_fixture,
        })
        project_result = db.session.execute(select_project_script, {
            'status_id': status_id
        }).fetchone()
        project_id = project_result.id

        # Inserir usuário
        db.session.execute(insert_user, {
            'cpf': cpf.value,
            'password': password.hashed_password,
            'salt': password.salt,
            'role': role.value,
            'email': email.email,
            'created_at': datetime_fixture,
        })

        # Inserir user_project manualmente
        db.session.execute(insert_user_project, {
            'user_cpf': cpf.value,
            'project_id': project_id,
            'assignment_date': datetime_fixture
        })
        db.session.commit()

    # Testar método find_all
    repo = UserProjectRepository(db_connection_handler)
    result = repo.find_all()

    assert isinstance(result, list)
    assert len(result) > 0
    assert any(
        r.cpf == cpf.value and r.project_id == project_id
        for r in result
    )

def test_update(
    insert_status_script,
    select_status_script,
    monetary_value,
    andamento_do_projeto,
    datetime_fixture,
    insert_project_script,
    select_project_script,
    insert_user,
    cpf,
    password,
    email,
    role,
    insert_user_project,
    select_user_project
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())

    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Ativo',
            'created_at': datetime_fixture
        })
        status_result = db.session.execute(select_status_script).fetchone()
        status_id = status_result.id

        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status_id,
            'verba_disponivel': monetary_value.value,
            'andamento_do_projeto': andamento_do_projeto,
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': datetime_fixture,
        })
        project_result = db.session.execute(select_project_script, {
            'status_id': status_id
        }).fetchone()
        project_id = project_result.id

        # Inserir usuário
        db.session.execute(insert_user, {
            'cpf': cpf.value,
            'password': password.hashed_password,
            'salt': password.salt,
            'role': role.value,
            'email': email.email,
            'created_at': datetime_fixture,
        })

        # Inserir user_project manualmente
        db.session.execute(insert_user_project, {
            'user_cpf': cpf.value,
            'project_id': project_id,
            'assignment_date': datetime_fixture
        })
        db.session.commit()

    # Novo valor de data para atualização
    new_assignment_date = datetime_fixture.replace(year=2030)

    # Testar método update
    repo = UserProjectRepository(db_connection_handler)
    repo.update(cpf, project_id, {"assignment_date": new_assignment_date})

    with db_connection_handler as db:
        result = db.session.execute(select_user_project, {
            'user_cpf': cpf.value,
            'project_id': project_id
        }).fetchone()

        assert result is not None
        assert result.assignment_date.year == new_assignment_date.year

def test_delete(
    insert_status_script,
    select_status_script,
    monetary_value,
    andamento_do_projeto,
    datetime_fixture,
    insert_project_script,
    select_project_script,
    insert_user,
    cpf,
    password,
    email,
    role,
    insert_user_project,
    select_user_project
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())

    with db_connection_handler as db:
        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Ativo',
            'created_at': datetime_fixture
        })
        status_result = db.session.execute(select_status_script).fetchone()
        status_id = status_result.id

        # Inserir projeto
        db.session.execute(insert_project_script, {
            'status_id': status_id,
            'verba_disponivel': monetary_value.value,
            'andamento_do_projeto': andamento_do_projeto,
            'start_date': datetime_fixture,
            'expected_completion_date': datetime_fixture,
            'end_date': datetime_fixture,
        })
        project_result = db.session.execute(select_project_script, {
            'status_id': status_id
        }).fetchone()
        project_id = project_result.id

        # Inserir usuário
        db.session.execute(insert_user, {
            'cpf': cpf.value,
            'password': password.hashed_password,
            'salt': password.salt,
            'role': role.value,
            'email': email.email,
            'created_at': datetime_fixture,
        })

        # Inserir user_project manualmente
        db.session.execute(insert_user_project, {
            'user_cpf': cpf.value,
            'project_id': project_id,
            'assignment_date': datetime_fixture
        })
        db.session.commit()

    # Instanciar o repositório
    repo = UserProjectRepository(db_connection_handler)

    # Verificar se a relação existe antes de deletar
    with db_connection_handler as db:
        result_before = db.session.execute(select_user_project, {
            'user_cpf': cpf.value,
            'project_id': project_id
        }).fetchone()
        assert result_before is not None

    # Executar o delete
    repo.delete(cpf, project_id)

    # Verificar se a relação foi removida
    with db_connection_handler as db:
        result_after = db.session.execute(select_user_project, {
            'user_cpf': cpf.value,
            'project_id': project_id
        }).fetchone()
        assert result_after is None

def test_find_all_from_cpf(
    insert_status_script,
    select_status_script,
    monetary_value,
    datetime_fixture,
    insert_project_script,
    select_project_script,
    insert_user,
    cpf,
    password,
    email,
    role,
    insert_user_project
) -> None:
    db_connection_handler = DBConnectionHandler(StringConnection())
    
    with db_connection_handler as db:

        # Inserir usuário
        db.session.execute(insert_user, {
            'cpf': cpf.value,
            'password': password.hashed_password,
            'salt': password.salt,
            'role': role.value,
            'email': email.email,
            'created_at': datetime_fixture,
        })

        db.session.commit()

        # Inserir status
        db.session.execute(insert_status_script, {
            'description': 'Ativo',
            'created_at': datetime_fixture
        })
        status_result = db.session.execute(select_status_script).fetchone()
        status_id = status_result.id

        project_ids = []

        # Criar 4 projetos e associar ao usuário sem repetir ID
        for i in range(1, 5):
            # Inserir novo projeto
            db.session.execute(insert_project_script, {
                'status_id': status_id,
                'verba_disponivel': monetary_value.value,
                'andamento_do_projeto': f'Andamento {i}',
                'start_date': datetime_fixture,
                'expected_completion_date': datetime_fixture,
                'end_date': datetime_fixture,
            })
            db.session.commit()

            # Buscar todos os projetos com este status
            all_projects = db.session.execute(select_project_script, {
                'status_id': status_id
            }).fetchall()

            # Encontrar um ID ainda não usado
            for project in all_projects:
                if project.id not in project_ids:
                    project_id = project.id
                    break

            # Adicionar à lista e associar ao usuário
            project_ids.append(project_id)

            db.session.execute(insert_user_project, {
                'user_cpf': cpf.value,
                'project_id': project_id,
                'assignment_date': datetime_fixture
            })

                # --- Asserts ---

        # Buscar projetos associados ao usuário
        result = db.session.execute(
        text("""
        SELECT up.project_id, p.andamento_do_projeto
        FROM user_project up
        JOIN project p ON p.id = up.project_id
        WHERE up.user_cpf = :cpf
        """),
        {'cpf': cpf.value}
        ).fetchall()


        assert len(result) == 4, "Usuário deveria estar associado a 4 projetos"
        
        # IDs únicos
        associated_project_ids = [row.project_id for row in result]
        assert len(set(associated_project_ids)) == 4, "IDs dos projetos associados devem ser únicos"

        # Verifica os andamentos esperados
        expected_andamentos = {f"Andamento {i}" for i in range(1, 5)}
        actual_andamentos = {row.andamento_do_projeto for row in result}
        assert actual_andamentos == expected_andamentos, "Andamentos dos projetos não correspondem aos esperados"