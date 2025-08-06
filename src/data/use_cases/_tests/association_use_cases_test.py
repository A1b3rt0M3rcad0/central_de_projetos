#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.associate_vereador_with_a_project import AssociateVereadorWithAProject
from src.data.use_cases.update_association_from_project import UpdateAssociationFromProject
from src.data.use_cases.delete_association_user_from_project import DeleteAssociationUserFromProject
from src.domain.value_objects.cpf import CPF
from src.domain.entities.user import UserEntity
from src.domain.value_objects.roles import Role
from src.errors.use_cases.invalid_role_error import InvalidRoleError
from src.errors.use_cases.user_not_found_error import UserNotFoundError
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError
from src.errors.use_cases.invalid_association_error import InvalidAssociationError
from src.errors.use_cases.association_not_found_error import AssociationNotFoundError
from src.errors.repository.already_exists_error.user_project_already_exists import UserProjectAlreadyExists
from src.errors.repository.already_exists_error.user_project_not_exists import UserProjectNotExists

@pytest.fixture
def mock_user_project_repository():
    return MagicMock()

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def mock_project_repository():
    return MagicMock()

@pytest.fixture
def valid_cpf():
    return CPF("12345678909")

@pytest.fixture
def vereador_user():
    from datetime import datetime
    from src.domain.value_objects.email import Email
    return UserEntity(
        cpf=CPF("12345678909"),
        password=b"password",
        salt=b"salt",
        role=Role("VEREADOR"),
        email=Email("test@example.com"),
        created_at=datetime.now(),
        name="Test Vereador"
    )

@pytest.fixture
def non_vereador_user():
    from datetime import datetime
    from src.domain.value_objects.email import Email
    return UserEntity(
        cpf=CPF("13265213064"),
        password=b"password",
        salt=b"salt",
        role=Role("ADMIN"),
        email=Email("user@example.com"),
        created_at=datetime.now(),
        name="Test User"
    )

def test_associate_vereador_with_a_project_success(mock_user_project_repository, mock_user_repository, mock_project_repository, valid_cpf, vereador_user):
    mock_user_repository.find.return_value = vereador_user
    mock_project_repository.find.return_value = MagicMock()
    
    use_case = AssociateVereadorWithAProject(mock_user_project_repository, mock_user_repository, mock_project_repository)
    use_case.associate(valid_cpf, 1)
    
    mock_user_repository.find.assert_called_once_with(valid_cpf)
    mock_project_repository.find.assert_called_once_with(project_id=1)
    mock_user_project_repository.insert.assert_called_once_with(cpf_user=valid_cpf, project_id=1)

def test_associate_vereador_with_a_project_invalid_role(mock_user_project_repository, mock_user_repository, mock_project_repository, valid_cpf, non_vereador_user):
    mock_user_repository.find.return_value = non_vereador_user
    
    use_case = AssociateVereadorWithAProject(mock_user_project_repository, mock_user_repository, mock_project_repository)
    
    with pytest.raises(InvalidRoleError):
        use_case.associate(valid_cpf, 1)

def test_associate_vereador_with_a_project_user_not_found(mock_user_project_repository, mock_user_repository, mock_project_repository, valid_cpf):
    mock_user_repository.find.side_effect = AttributeError("User not found")
    
    use_case = AssociateVereadorWithAProject(mock_user_project_repository, mock_user_repository, mock_project_repository)
    
    with pytest.raises(UserNotFoundError):
        use_case.associate(valid_cpf, 1)

def test_associate_vereador_with_a_project_project_not_found(mock_user_project_repository, mock_user_repository, mock_project_repository, valid_cpf, vereador_user):
    mock_user_repository.find.return_value = vereador_user
    mock_project_repository.find.side_effect = AttributeError("Project not found")
    
    use_case = AssociateVereadorWithAProject(mock_user_project_repository, mock_user_repository, mock_project_repository)
    
    with pytest.raises(ProjectNotFoundError, match="Project with id 1 not founded"):
        use_case.associate(valid_cpf, 1)

def test_associate_vereador_with_a_project_already_exists(mock_user_project_repository, mock_user_repository, mock_project_repository, valid_cpf, vereador_user):
    mock_user_repository.find.return_value = vereador_user
    mock_project_repository.find.return_value = MagicMock()
    mock_user_project_repository.insert.side_effect = UserProjectAlreadyExists("Association already exists")
    
    use_case = AssociateVereadorWithAProject(mock_user_project_repository, mock_user_repository, mock_project_repository)
    
    with pytest.raises(InvalidAssociationError, match="This association already exists"):
        use_case.associate(valid_cpf, 1)

def test_update_association_from_project_success(mock_user_project_repository, mock_user_repository, valid_cpf, vereador_user):
    mock_user_repository.find.return_value = vereador_user
    mock_user_project_repository.find.return_value = MagicMock()
    
    new_cpf = CPF("13265213064")
    use_case = UpdateAssociationFromProject(mock_user_project_repository, mock_user_repository)
    use_case.update(valid_cpf, 1, new_cpf)
    
    mock_user_repository.find.assert_called_once_with(cpf=new_cpf)
    mock_user_project_repository.find.assert_called_once_with(cpf_user=valid_cpf, project_id=1)
    mock_user_project_repository.update.assert_called_once_with(
        cpf_user=valid_cpf, 
        project_id=1, 
        update_params={'cpf': new_cpf.value}
    )

def test_update_association_from_project_invalid_role(mock_user_project_repository, mock_user_repository, valid_cpf, non_vereador_user):
    mock_user_repository.find.return_value = non_vereador_user
    
    new_cpf = CPF("13265213064")
    use_case = UpdateAssociationFromProject(mock_user_project_repository, mock_user_repository)
    
    with pytest.raises(InvalidRoleError):
        use_case.update(valid_cpf, 1, new_cpf)

def test_update_association_from_project_user_not_found(mock_user_project_repository, mock_user_repository, valid_cpf):
    mock_user_repository.find.side_effect = RuntimeError("User not found")
    
    new_cpf = CPF("13265213064")
    use_case = UpdateAssociationFromProject(mock_user_project_repository, mock_user_repository)
    
    with pytest.raises(UserNotFoundError):
        use_case.update(valid_cpf, 1, new_cpf)

def test_update_association_from_project_association_not_found(mock_user_project_repository, mock_user_repository, valid_cpf, vereador_user):
    mock_user_repository.find.return_value = vereador_user
    mock_user_project_repository.find.side_effect = UserProjectNotExists("Association not found")
    
    new_cpf = CPF("13265213064")
    use_case = UpdateAssociationFromProject(mock_user_project_repository, mock_user_repository)
    
    with pytest.raises(AssociationNotFoundError, match="Association not founded"):
        use_case.update(valid_cpf, 1, new_cpf)

def test_delete_association_user_from_project_success(mock_user_project_repository):
    use_case = DeleteAssociationUserFromProject(mock_user_project_repository)
    use_case.delete(1)
    
    mock_user_project_repository.delete_all_from_project.assert_called_once_with(project_id=1)

def test_delete_association_user_from_project_repository_error(mock_user_project_repository):
    mock_user_project_repository.delete_all_from_project.side_effect = Exception("Repository error")
    
    use_case = DeleteAssociationUserFromProject(mock_user_project_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1) 