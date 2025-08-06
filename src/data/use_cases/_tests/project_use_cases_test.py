#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.create_project import CreateProject
from src.data.use_cases.find_project_by_name import FindProjectByName
from src.data.use_cases.delete_project import DeleteProject
from src.data.use_cases.count_projects import CountProjects
from src.data.use_cases.find_all_projects_with_basic_details import FindAllProjectsWithBasicDetails
from src.data.use_cases.find_all_from_project import FindAllFromProject
from src.data.use_cases.find_all_projects_from_empresa import FindAllProjectsFromEmpresa
from src.data.use_cases.find_all_projects_from_bairro import FindAllProjectsFromBairro
from src.domain.entities.project import ProjectEntity
from src.domain.entities.project_empresa import ProjectEmpresaEntity
from src.domain.entities.project_bairro import ProjectBairroEntity
from src.errors.repository.error_on_find.error_on_find_project import ErrorOnFindProject

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def mock_project_empresa_repository():
    return MagicMock()

@pytest.fixture
def mock_project_bairro_repository():
    return MagicMock()

@pytest.fixture
def project_entity():
    from datetime import datetime
    from src.domain.value_objects.monetary_value import MonetaryValue
    return ProjectEntity(
        project_id=1,
        status_id=1,
        verba_disponivel=MonetaryValue(1000.0),
        andamento_do_projeto="Em andamento",
        start_date=datetime.now(),
        expected_completion_date=datetime.now(),
        end_date=datetime.now(),
        name="Test Project"
    )

@pytest.fixture
def project_empresa_entity():
    from datetime import datetime
    return ProjectEmpresaEntity(
        project_id=1,
        empresa_id=1,
        created_at=datetime.now()
    )

@pytest.fixture
def project_bairro_entity():
    from datetime import datetime
    return ProjectBairroEntity(
        project_id=1,
        bairro_id=1,
        created_at=datetime.now()
    )

def test_create_project_success(mock_repository):
    use_case = CreateProject(mock_repository)
    use_case.create(1, "Test Project")
    
    mock_repository.insert.assert_called_once_with(
        status_id=1,
        name="Test Project",
        verba_disponivel=None,
        andamento_do_projeto=None,
        start_date=None,
        expected_completion_date=None,
        end_date=None
    )

def test_create_project_repository_error(mock_repository):
    mock_repository.insert.side_effect = Exception("Repository error")
    
    use_case = CreateProject(mock_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.create(1, "Test Project")

def test_find_project_by_name_success(mock_repository, project_entity):
    mock_repository.find_by_name.return_value = project_entity
    
    use_case = FindProjectByName(mock_repository)
    result = use_case.find("Test Project")
    
    mock_repository.find_by_name.assert_called_once_with(name="Test Project")
    assert result == project_entity

def test_find_project_by_name_not_found(mock_repository):
    mock_repository.find_by_name.return_value = None
    
    use_case = FindProjectByName(mock_repository)
    result = use_case.find("Non Existent Project")
    
    mock_repository.find_by_name.assert_called_once_with(name="Non Existent Project")
    assert result is None

def test_delete_project_success(mock_repository):
    use_case = DeleteProject(mock_repository)
    use_case.delete(1)
    
    mock_repository.delete.assert_called_once_with(project_id=1)

def test_delete_project_repository_error(mock_repository):
    mock_repository.delete.side_effect = Exception("Repository error")
    
    use_case = DeleteProject(mock_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1)

def test_count_projects_success(mock_repository):
    mock_repository.count_projects.return_value = {"count": 5}
    
    use_case = CountProjects(mock_repository)
    result = use_case.count()
    
    mock_repository.count_projects.assert_called_once()
    assert result == {"count": 5}

def test_find_all_projects_with_basic_details_success(mock_repository, project_entity):
    mock_repository.find_all_projects_with_basic_details.return_value = [project_entity]
    
    use_case = FindAllProjectsWithBasicDetails(mock_repository)
    result = use_case.find()
    
    mock_repository.find_all_projects_with_basic_details.assert_called_once()
    assert result == [project_entity]

def test_find_all_projects_with_basic_details_empty_list(mock_repository):
    mock_repository.find_all_projects_with_basic_details.return_value = []
    
    use_case = FindAllProjectsWithBasicDetails(mock_repository)
    result = use_case.find()
    
    mock_repository.find_all_projects_with_basic_details.assert_called_once()
    assert result == []

def test_find_all_projects_with_basic_details_repository_error(mock_repository):
    mock_repository.find_all_projects_with_basic_details.side_effect = Exception("Repository error")
    
    use_case = FindAllProjectsWithBasicDetails(mock_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.find()

def test_find_all_from_project_success(mock_repository, project_entity):
    mock_repository.find_all_from_project.return_value = project_entity
    
    use_case = FindAllFromProject(mock_repository)
    result = use_case.find(1)
    
    mock_repository.find_all_from_project.assert_called_once_with(project_id=1)
    assert result == project_entity

def test_find_all_from_project_repository_error(mock_repository):
    mock_repository.find_all_from_project.side_effect = Exception("Repository error")
    
    use_case = FindAllFromProject(mock_repository)
    
    with pytest.raises(ErrorOnFindProject):
        use_case.find(1)

def test_find_all_projects_from_empresa_success(mock_project_empresa_repository, project_empresa_entity):
    mock_project_empresa_repository.find_all_from_empresa.return_value = [project_empresa_entity]
    
    use_case = FindAllProjectsFromEmpresa(mock_project_empresa_repository)
    result = use_case.find(1)
    
    mock_project_empresa_repository.find_all_from_empresa.assert_called_once_with(empresa_id=1)
    assert result == [project_empresa_entity]

def test_find_all_projects_from_empresa_empty_list(mock_project_empresa_repository):
    mock_project_empresa_repository.find_all_from_empresa.return_value = []
    
    use_case = FindAllProjectsFromEmpresa(mock_project_empresa_repository)
    result = use_case.find(1)
    
    mock_project_empresa_repository.find_all_from_empresa.assert_called_once_with(empresa_id=1)
    assert result == []

def test_find_all_projects_from_empresa_repository_error(mock_project_empresa_repository):
    mock_project_empresa_repository.find_all_from_empresa.side_effect = Exception("Repository error")
    
    use_case = FindAllProjectsFromEmpresa(mock_project_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.find(1)

def test_find_all_projects_from_bairro_success(mock_project_bairro_repository, project_bairro_entity):
    mock_project_bairro_repository.find_all_from_bairro.return_value = [project_bairro_entity]
    
    use_case = FindAllProjectsFromBairro(mock_project_bairro_repository)
    result = use_case.find(1)
    
    mock_project_bairro_repository.find_all_from_bairro.assert_called_once_with(bairro_id=1)
    assert result == [project_bairro_entity]

def test_find_all_projects_from_bairro_empty_list(mock_project_bairro_repository):
    mock_project_bairro_repository.find_all_from_bairro.return_value = []
    
    use_case = FindAllProjectsFromBairro(mock_project_bairro_repository)
    result = use_case.find(1)
    
    mock_project_bairro_repository.find_all_from_bairro.assert_called_once_with(bairro_id=1)
    assert result == []

def test_find_all_projects_from_bairro_repository_error(mock_project_bairro_repository):
    mock_project_bairro_repository.find_all_from_bairro.side_effect = Exception("Repository error")
    
    use_case = FindAllProjectsFromBairro(mock_project_bairro_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.find(1) 