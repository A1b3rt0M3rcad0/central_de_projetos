#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.create_user import CreateUser
from src.data.use_cases.update_user_email import UpdateUserEmail
from src.data.use_cases.find_all_user import FindAllUser
from src.data.use_cases.find_all_user_by_role import FindAllUserByRole
from src.domain.entities.user import UserEntity
from src.errors.repository.already_exists_error.user_already_exists import UserAlreadyExists
from src.errors.use_cases.create_user_error import CreateUserError
from src.errors.use_cases.email_already_exists_error import EmailAlreadyExistsError
from src.errors.repository.not_exists_error.user_not_exists import UserNotExists

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def user_entity():
    from datetime import datetime
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.email import Email
    from src.domain.value_objects.roles import Role
    return UserEntity(
        cpf=CPF("12345678909"),
        password=b"hashed_password",
        salt=b"salt_value",
        role=Role("ADMIN"),
        email=Email("teste@example.com"),
        created_at=datetime.now(),
        name="Usuário Teste"
    )

# Testes para CreateUser
def test_create_user_success(mock_user_repository):
    """Testa criação de usuário com sucesso"""
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.email import Email
    from src.domain.value_objects.password import Password
    from src.domain.value_objects.roles import Role
    
    use_case = CreateUser(mock_user_repository)
    
    use_case.create(
        cpf=CPF("12345678909"),
        email=Email("teste@example.com"),
        role=Role("ADMIN"),
        password=Password("Password123"),
        name="Usuário Teste"
    )
    
    mock_user_repository.insert.assert_called_once()
    call_args = mock_user_repository.insert.call_args
    assert call_args[1]['cpf'].value == "12345678909"
    assert call_args[1]['email'].email == "teste@example.com"
    assert call_args[1]['role'].value == "ADMIN"
    assert call_args[1]['name'] == "Usuário Teste"

def test_create_user_repository_error(mock_user_repository):
    """Testa criação de usuário quando repositório lança exceção"""
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.email import Email
    from src.domain.value_objects.password import Password
    from src.domain.value_objects.roles import Role
    
    mock_user_repository.insert.side_effect = UserAlreadyExists(message="Usuário já existe")
    use_case = CreateUser(mock_user_repository)
    
    with pytest.raises(CreateUserError):
        use_case.create(
            cpf=CPF("12345678909"),
            email=Email("teste@example.com"),
            role=Role("ADMIN"),
            password=Password("Password123"),
            name="Usuário Teste"
        )

# Testes para UpdateUserEmail
def test_update_user_email_success(mock_user_repository):
    """Testa atualização de email com sucesso"""
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.email import Email
    
    # Mock para simular que o email não existe
    mock_user_repository.find_by_email.side_effect = UserNotExists(message="Email não encontrado")
    
    use_case = UpdateUserEmail(mock_user_repository)
    
    use_case.update(
        cpf=CPF("12345678909"),
        email=Email("novo@example.com")
    )
    
    mock_user_repository.update.assert_called_once()
    call_args = mock_user_repository.update.call_args
    assert call_args[1]['cpf'].value == "12345678909"
    assert call_args[1]['update_params']['email'] == "novo@example.com"

def test_update_user_email_already_exists(mock_user_repository, user_entity):
    """Testa atualização de email quando email já existe"""
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.email import Email
    
    # Mock para simular que o email já existe
    mock_user_repository.find_by_email.return_value = user_entity
    
    use_case = UpdateUserEmail(mock_user_repository)
    
    with pytest.raises(EmailAlreadyExistsError):
        use_case.update(
            cpf=CPF("12345678909"),
            email=Email("existente@example.com")
        )

def test_update_user_email_repository_error(mock_user_repository):
    """Testa atualização de email quando repositório lança exceção"""
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.email import Email
    
    mock_user_repository.find_by_email.side_effect = Exception("Erro no repositório")
    
    use_case = UpdateUserEmail(mock_user_repository)
    
    with pytest.raises(Exception):
        use_case.update(
            cpf=CPF("12345678909"),
            email=Email("teste@example.com")
        )

# Testes para FindAllUser
def test_find_all_user_success(mock_user_repository, user_entity):
    """Testa busca de todos os usuários com sucesso"""
    mock_user_repository.find_all.return_value = [user_entity]
    use_case = FindAllUser(mock_user_repository)
    
    result = use_case.find()
    
    mock_user_repository.find_all.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], UserEntity)

def test_find_all_user_empty_list(mock_user_repository):
    """Testa busca de todos os usuários quando lista está vazia"""
    mock_user_repository.find_all.return_value = []
    use_case = FindAllUser(mock_user_repository)
    
    result = use_case.find()
    
    mock_user_repository.find_all.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 0

def test_find_all_user_repository_error(mock_user_repository):
    """Testa busca de todos os usuários quando repositório lança exceção"""
    mock_user_repository.find_all.side_effect = Exception("Erro no repositório")
    use_case = FindAllUser(mock_user_repository)
    
    with pytest.raises(Exception):
        use_case.find()

# Testes para FindAllUserByRole
def test_find_all_user_by_role_success(mock_user_repository, user_entity):
    """Testa busca de usuários por role com sucesso"""
    from src.domain.value_objects.roles import Role
    
    mock_user_repository.find_all_by_role.return_value = [user_entity]
    use_case = FindAllUserByRole(mock_user_repository)
    
    result = use_case.find(role=Role("ADMIN"))
    
    mock_user_repository.find_all_by_role.assert_called_once_with(role=Role("ADMIN"))
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], UserEntity)

def test_find_all_user_by_role_empty_list(mock_user_repository):
    """Testa busca de usuários por role quando lista está vazia"""
    from src.domain.value_objects.roles import Role
    
    mock_user_repository.find_all_by_role.return_value = []
    use_case = FindAllUserByRole(mock_user_repository)
    
    result = use_case.find(role=Role("ASSESSOR"))
    
    mock_user_repository.find_all_by_role.assert_called_once_with(role=Role("ASSESSOR"))
    assert isinstance(result, list)
    assert len(result) == 0

def test_find_all_user_by_role_repository_error(mock_user_repository):
    """Testa busca de usuários por role quando repositório lança exceção"""
    from src.domain.value_objects.roles import Role
    
    mock_user_repository.find_all_by_role.side_effect = Exception("Erro no repositório")
    use_case = FindAllUserByRole(mock_user_repository)
    
    with pytest.raises(Exception):
        use_case.find(role=Role("ADMIN")) 