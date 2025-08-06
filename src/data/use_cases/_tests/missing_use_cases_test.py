#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.find_user_by_project_id import FindUserByProjectId
from src.data.use_cases.get_count_projects_by_user import GetCountProjectsByUser
from src.data.use_cases.get_count_projects_by_empresas import GetCountProjectsByEmpresas
from src.data.use_cases.get_count_projects_by_fiscal import GetCountProjectsByFiscal
from src.data.use_cases.get_project_types_count_by_bairro import GetProjectTypesCountByBairro
from src.data.use_cases.get_project_counts_by_bairro import GetProjectCountsByBairro
from src.data.use_cases.get_project_status_count_by_bairro import GetProjectStatusCountByBairro
from src.data.use_cases.get_project_verba_by_bairro import GetProjectVerbaByBairro
from src.data.use_cases.delete_all_history_project_from_project import DeleteAllHistoryProjectFromProject
from src.data.use_cases.delete_history_project import DeleteHistoryProject
from src.data.use_cases.delete_project_type import DeleteProjectType
from src.domain.entities.user import UserEntity
from src.domain.entities.project_types_count_by_bairro import ProjectTypesCountByBairro
from src.domain.entities.project_bairro_summary import ProjectBairroSummary
from src.domain.entities.project_bairro_status_summary import ProjectBairroStatusSummary
from src.domain.entities.project_bairro_verba_summary import ProjectBairroVerbaSummary

@pytest.fixture
def mock_user_project_repository():
    return MagicMock()

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def mock_empresa_repository():
    return MagicMock()

@pytest.fixture
def mock_project_fiscal_repository():
    return MagicMock()

@pytest.fixture
def mock_project_type_repository():
    return MagicMock()

@pytest.fixture
def mock_project_bairro_repository():
    return MagicMock()

@pytest.fixture
def mock_history_project_repository():
    return MagicMock()

@pytest.fixture
def user_entity():
    from datetime import datetime
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.email import Email
    from src.domain.value_objects.roles import Role
    return UserEntity(
        cpf=CPF("12345678909"),
        password=b"password",
        salt=b"salt",
        role=Role("ADMIN"),
        email=Email("test@example.com"),
        created_at=datetime.now(),
        name="Test User"
    )

@pytest.fixture
def project_types_count_by_bairro_entity():
    return ProjectTypesCountByBairro(
        bairro_id=1,
        bairro_name="Test Bairro",
        types_count=5
    )

@pytest.fixture
def project_bairro_summary_entity():
    return ProjectBairroSummary(
        bairro_id=1,
        bairro_name="Test Bairro",
        project_count=10
    )

@pytest.fixture
def project_bairro_status_summary_entity():
    return ProjectBairroStatusSummary(
        bairro_id=1,
        bairro_name="Test Bairro",
        status_count=3
    )

@pytest.fixture
def project_bairro_verba_summary_entity():
    return ProjectBairroVerbaSummary(
        bairro_id=1,
        bairro_name="Test Bairro",
        total_verba=100000.0
    )

def test_find_user_by_project_id_success(mock_user_project_repository, user_entity):
    mock_user_project_repository.find_user_by_project_id.return_value = user_entity
    
    use_case = FindUserByProjectId(mock_user_project_repository)
    result = use_case.find(1)
    
    mock_user_project_repository.find_user_by_project_id.assert_called_once_with(project_id=1)
    assert result == user_entity

def test_find_user_by_project_id_none(mock_user_project_repository):
    mock_user_project_repository.find_user_by_project_id.return_value = None
    
    use_case = FindUserByProjectId(mock_user_project_repository)
    result = use_case.find(1)
    
    mock_user_project_repository.find_user_by_project_id.assert_called_once_with(project_id=1)
    assert result is None

def test_find_user_by_project_id_repository_error(mock_user_project_repository):
    mock_user_project_repository.find_user_by_project_id.side_effect = Exception("Repository error")
    
    use_case = FindUserByProjectId(mock_user_project_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.find(1)

def test_get_count_projects_by_user_success(mock_user_repository):
    mock_user_repository.get_count_projects_by_user.return_value = {"count": 5}
    
    use_case = GetCountProjectsByUser(mock_user_repository)
    result = use_case.get()
    
    mock_user_repository.get_count_projects_by_user.assert_called_once()
    assert result == {"count": 5}

def test_get_count_projects_by_user_repository_error(mock_user_repository):
    mock_user_repository.get_count_projects_by_user.side_effect = Exception("Repository error")
    
    use_case = GetCountProjectsByUser(mock_user_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.get()

def test_get_count_projects_by_empresas_success(mock_empresa_repository):
    mock_empresa_repository.get_count_projects_by_empresas.return_value = {"count": 8}
    
    use_case = GetCountProjectsByEmpresas(mock_empresa_repository)
    result = use_case.get()
    
    mock_empresa_repository.get_count_projects_by_empresas.assert_called_once()
    assert result == {"count": 8}

def test_get_count_projects_by_empresas_repository_error(mock_empresa_repository):
    mock_empresa_repository.get_count_projects_by_empresas.side_effect = Exception("Repository error")
    
    use_case = GetCountProjectsByEmpresas(mock_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.get()

def test_get_count_projects_by_fiscal_success(mock_project_fiscal_repository):
    mock_project_fiscal_repository.get_count_projects_by_fiscal.return_value = {"count": 3}
    
    use_case = GetCountProjectsByFiscal(mock_project_fiscal_repository)
    result = use_case.get()
    
    mock_project_fiscal_repository.get_count_projects_by_fiscal.assert_called_once()
    assert result == {"count": 3}

def test_get_count_projects_by_fiscal_repository_error(mock_project_fiscal_repository):
    mock_project_fiscal_repository.get_count_projects_by_fiscal.side_effect = Exception("Repository error")
    
    use_case = GetCountProjectsByFiscal(mock_project_fiscal_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.get()

def test_get_project_types_count_by_bairro_success(mock_project_type_repository, project_types_count_by_bairro_entity):
    mock_project_type_repository.get_project_types_count_by_bairro.return_value = project_types_count_by_bairro_entity
    
    use_case = GetProjectTypesCountByBairro(mock_project_type_repository)
    result = use_case.get()
    
    mock_project_type_repository.get_project_types_count_by_bairro.assert_called_once()
    assert result == project_types_count_by_bairro_entity

def test_get_project_types_count_by_bairro_repository_error(mock_project_type_repository):
    mock_project_type_repository.get_project_types_count_by_bairro.side_effect = Exception("Repository error")
    
    use_case = GetProjectTypesCountByBairro(mock_project_type_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.get()

def test_get_project_counts_by_bairro_success(mock_project_bairro_repository, project_bairro_summary_entity):
    mock_project_bairro_repository.get_project_counts_by_bairro.return_value = project_bairro_summary_entity
    
    use_case = GetProjectCountsByBairro(mock_project_bairro_repository)
    result = use_case.get()
    
    mock_project_bairro_repository.get_project_counts_by_bairro.assert_called_once()
    assert result == project_bairro_summary_entity

def test_get_project_counts_by_bairro_repository_error(mock_project_bairro_repository):
    mock_project_bairro_repository.get_project_counts_by_bairro.side_effect = Exception("Repository error")
    
    use_case = GetProjectCountsByBairro(mock_project_bairro_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.get()

def test_get_project_status_count_by_bairro_success(mock_project_bairro_repository, project_bairro_status_summary_entity):
    mock_project_bairro_repository.get_project_status_count_by_bairro.return_value = project_bairro_status_summary_entity
    
    use_case = GetProjectStatusCountByBairro(mock_project_bairro_repository)
    result = use_case.get()
    
    mock_project_bairro_repository.get_project_status_count_by_bairro.assert_called_once()
    assert result == project_bairro_status_summary_entity

def test_get_project_status_count_by_bairro_repository_error(mock_project_bairro_repository):
    mock_project_bairro_repository.get_project_status_count_by_bairro.side_effect = Exception("Repository error")
    
    use_case = GetProjectStatusCountByBairro(mock_project_bairro_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.get()

def test_get_project_verba_by_bairro_success(mock_project_bairro_repository, project_bairro_verba_summary_entity):
    mock_project_bairro_repository.get_project_verba_by_bairro.return_value = project_bairro_verba_summary_entity
    
    use_case = GetProjectVerbaByBairro(mock_project_bairro_repository)
    result = use_case.get()
    
    mock_project_bairro_repository.get_project_verba_by_bairro.assert_called_once()
    assert result == project_bairro_verba_summary_entity

def test_get_project_verba_by_bairro_repository_error(mock_project_bairro_repository):
    mock_project_bairro_repository.get_project_verba_by_bairro.side_effect = Exception("Repository error")
    
    use_case = GetProjectVerbaByBairro(mock_project_bairro_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.get()

def test_delete_all_history_project_from_project_success(mock_history_project_repository):
    use_case = DeleteAllHistoryProjectFromProject(mock_history_project_repository)
    use_case.delete(1)
    
    mock_history_project_repository.delete_all_from_project.assert_called_once_with(project_id=1)

def test_delete_all_history_project_from_project_repository_error(mock_history_project_repository):
    mock_history_project_repository.delete_all_from_project.side_effect = Exception("Repository error")
    
    use_case = DeleteAllHistoryProjectFromProject(mock_history_project_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1)

def test_delete_history_project_success(mock_history_project_repository):
    use_case = DeleteHistoryProject(mock_history_project_repository)
    use_case.delete(1)
    
    mock_history_project_repository.delete.assert_called_once_with(history_project_id=1)

def test_delete_history_project_repository_error(mock_history_project_repository):
    mock_history_project_repository.delete.side_effect = Exception("Repository error")
    
    use_case = DeleteHistoryProject(mock_history_project_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1)

def test_delete_project_type_success(mock_project_type_repository):
    use_case = DeleteProjectType(mock_project_type_repository)
    use_case.delete(1, 2)
    
    mock_project_type_repository.delete.assert_called_once_with(project_id=1, type_id=2)

def test_delete_project_type_repository_error(mock_project_type_repository):
    mock_project_type_repository.delete.side_effect = Exception("Repository error")
    
    use_case = DeleteProjectType(mock_project_type_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1, 2) 