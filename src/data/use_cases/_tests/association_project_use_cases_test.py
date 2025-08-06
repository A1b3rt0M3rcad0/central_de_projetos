#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.associate_vereador_with_a_project import AssociateVereadorWithAProject
from src.data.use_cases.update_association_from_project import UpdateAssociationFromProject
from src.domain.entities.user import UserEntity
from src.domain.entities.project import ProjectEntity
from src.errors.use_cases.invalid_role_error import InvalidRoleError
from src.errors.use_cases.user_not_found_error import UserNotFoundError
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError
from src.errors.repository.already_exists_error.user_project_already_exists import UserProjectAlreadyExists
from src.errors.use_cases.invalid_association_error import InvalidAssociationError
from src.errors.use_cases.association_not_found_error import AssociationNotFoundError
from src.errors.repository.already_exists_error.user_project_not_exists import UserProjectNotExists

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def mock_project_repository():
    return MagicMock()

@pytest.fixture
def mock_user_project_repository():
    return MagicMock()

@pytest.fixture
def vereador_entity():
    from datetime import datetime
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.email import Email
    from src.domain.value_objects.roles import Role
    return UserEntity(
        cpf=CPF("12345678909"),
        password=b"hashed_password",
        salt=b"salt_value",
        role=Role("VEREADOR"),
        email=Email("vereador@example.com"),
        created_at=datetime.now(),
        name="Vereador Teste"
    )

@pytest.fixture
def project_entity():
    from datetime import datetime
    from src.domain.value_objects.monetary_value import MonetaryValue
    return ProjectEntity(
        project_id=1,
        status_id=1,
        verba_disponivel=MonetaryValue(10000.0),
        andamento_do_projeto="Em andamento",
        start_date=datetime.now(),
        expected_completion_date=datetime.now(),
        end_date=datetime.now(),
        name="Projeto Teste"
    )

# Testes para AssociateVereadorWithAProject
def test_associate_vereador_with_project_success(mock_user_project_repository, mock_user_repository, mock_project_repository, vereador_entity, project_entity):
    """Testa associação de vereador com projeto com sucesso"""
    from src.domain.value_objects.cpf import CPF
    
    mock_user_repository.find.return_value = vereador_entity
    mock_project_repository.find.return_value = project_entity
    
    use_case = AssociateVereadorWithAProject(
        user_project_repository=mock_user_project_repository,
        user_repository=mock_user_repository,
        project_repository=mock_project_repository
    )
    
    use_case.associate(cpf_user=CPF("12345678909"), project_id=1)
    
    mock_user_repository.find.assert_called_once()
    call_args = mock_user_repository.find.call_args
    assert call_args[0][0].value == "12345678909"
    mock_project_repository.find.assert_called_once_with(project_id=1)
    mock_user_project_repository.insert.assert_called_once()
    call_args = mock_user_project_repository.insert.call_args
    assert call_args[1]['cpf_user'].value == "12345678909"
    assert call_args[1]['project_id'] == 1

def test_associate_vereador_with_project_invalid_role(mock_user_project_repository, mock_user_repository, mock_project_repository):
    """Testa associação quando usuário não é vereador"""
    from src.domain.value_objects.cpf import CPF
    from datetime import datetime
    from src.domain.value_objects.email import Email
    from src.domain.value_objects.roles import Role
    
    # Criar usuário com role inválida
    user_invalid_role = UserEntity(
        cpf=CPF("12345678909"),
        password=b"hashed_password",
        salt=b"salt_value",
        role=Role("ADMIN"),
        email=Email("admin@example.com"),
        created_at=datetime.now(),
        name="Admin Teste"
    )
    
    mock_user_repository.find.return_value = user_invalid_role
    
    use_case = AssociateVereadorWithAProject(
        user_project_repository=mock_user_project_repository,
        user_repository=mock_user_repository,
        project_repository=mock_project_repository
    )
    
    with pytest.raises(InvalidRoleError):
        use_case.associate(cpf_user=CPF("12345678909"), project_id=1)

def test_associate_vereador_with_project_user_not_found(mock_user_project_repository, mock_user_repository, mock_project_repository):
    """Testa associação quando usuário não encontrado"""
    from src.domain.value_objects.cpf import CPF
    
    mock_user_repository.find.side_effect = AttributeError("Usuário não encontrado")
    
    use_case = AssociateVereadorWithAProject(
        user_project_repository=mock_user_project_repository,
        user_repository=mock_user_repository,
        project_repository=mock_project_repository
    )
    
    with pytest.raises(UserNotFoundError):
        use_case.associate(cpf_user=CPF("12345678909"), project_id=1)

def test_associate_vereador_with_project_project_not_found(mock_user_project_repository, mock_user_repository, mock_project_repository, vereador_entity):
    """Testa associação quando projeto não encontrado"""
    from src.domain.value_objects.cpf import CPF
    
    mock_user_repository.find.return_value = vereador_entity
    mock_project_repository.find.side_effect = AttributeError("Projeto não encontrado")
    
    use_case = AssociateVereadorWithAProject(
        user_project_repository=mock_user_project_repository,
        user_repository=mock_user_repository,
        project_repository=mock_project_repository
    )
    
    with pytest.raises(ProjectNotFoundError):
        use_case.associate(cpf_user=CPF("12345678909"), project_id=999)

def test_associate_vereador_with_project_already_exists(mock_user_project_repository, mock_user_repository, mock_project_repository, vereador_entity, project_entity):
    """Testa associação quando associação já existe"""
    from src.domain.value_objects.cpf import CPF
    
    mock_user_repository.find.return_value = vereador_entity
    mock_project_repository.find.return_value = project_entity
    mock_user_project_repository.insert.side_effect = UserProjectAlreadyExists(message="Associação já existe")
    
    use_case = AssociateVereadorWithAProject(
        user_project_repository=mock_user_project_repository,
        user_repository=mock_user_repository,
        project_repository=mock_project_repository
    )
    
    with pytest.raises(InvalidAssociationError):
        use_case.associate(cpf_user=CPF("12345678909"), project_id=1)

# Testes para UpdateAssociationFromProject
def test_update_association_from_project_success(mock_user_project_repository, mock_user_repository, vereador_entity):
    """Testa atualização de associação com sucesso"""
    from src.domain.value_objects.cpf import CPF
    
    mock_user_repository.find.return_value = vereador_entity
    mock_user_project_repository.find.return_value = {"cpf": "12345678909", "project_id": 1}
    
    use_case = UpdateAssociationFromProject(
        user_project_repository=mock_user_project_repository,
        user_repository=mock_user_repository
    )
    
    use_case.update(cpf=CPF("12345678909"), project_id=1, new_cpf=CPF("98765432100"))
    
    mock_user_repository.find.assert_called_once()
    call_args = mock_user_repository.find.call_args
    assert call_args[1]['cpf'].value == "98765432100"
    mock_user_project_repository.find.assert_called_once()
    call_args = mock_user_project_repository.find.call_args
    assert call_args[1]['cpf_user'].value == "12345678909"
    assert call_args[1]['project_id'] == 1
    mock_user_project_repository.update.assert_called_once()
    call_args = mock_user_project_repository.update.call_args
    assert call_args[1]['cpf_user'].value == "12345678909"
    assert call_args[1]['project_id'] == 1
    assert call_args[1]['update_params']['cpf'] == "98765432100"

def test_update_association_from_project_invalid_role(mock_user_project_repository, mock_user_repository):
    """Testa atualização quando novo usuário não é vereador"""
    from src.domain.value_objects.cpf import CPF
    from datetime import datetime
    from src.domain.value_objects.email import Email
    from src.domain.value_objects.roles import Role
    
    # Criar usuário com role inválida
    user_invalid_role = UserEntity(
        cpf=CPF("98765432100"),
        password=b"hashed_password",
        salt=b"salt_value",
        role=Role("ADMIN"),
        email=Email("admin@example.com"),
        created_at=datetime.now(),
        name="Admin Teste"
    )
    
    mock_user_repository.find.return_value = user_invalid_role
    
    use_case = UpdateAssociationFromProject(
        user_project_repository=mock_user_project_repository,
        user_repository=mock_user_repository
    )
    
    with pytest.raises(InvalidRoleError):
        use_case.update(cpf=CPF("12345678909"), project_id=1, new_cpf=CPF("98765432100"))

def test_update_association_from_project_user_not_found(mock_user_project_repository, mock_user_repository):
    """Testa atualização quando novo usuário não encontrado"""
    from src.domain.value_objects.cpf import CPF
    
    mock_user_repository.find.side_effect = RuntimeError("Usuário não encontrado")
    
    use_case = UpdateAssociationFromProject(
        user_project_repository=mock_user_project_repository,
        user_repository=mock_user_repository
    )
    
    with pytest.raises(UserNotFoundError):
        use_case.update(cpf=CPF("12345678909"), project_id=1, new_cpf=CPF("98765432100"))

def test_update_association_from_project_association_not_found(mock_user_project_repository, mock_user_repository, vereador_entity):
    """Testa atualização quando associação não encontrada"""
    from src.domain.value_objects.cpf import CPF
    
    mock_user_repository.find.return_value = vereador_entity
    mock_user_project_repository.find.side_effect = UserProjectNotExists(message="Associação não encontrada")
    
    use_case = UpdateAssociationFromProject(
        user_project_repository=mock_user_project_repository,
        user_repository=mock_user_repository
    )
    
    with pytest.raises(AssociationNotFoundError):
        use_case.update(cpf=CPF("12345678909"), project_id=1, new_cpf=CPF("98765432100")) 