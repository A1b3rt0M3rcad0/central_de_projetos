#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.delete_type import DeleteType
from src.data.use_cases.find_type_from_project import FindTypeFromProject
from src.data.use_cases.delete_type_from_project import DeleteTypeFromProject
from src.data.use_cases.create_project_type import CreateProjectType
from src.domain.entities.project_types import ProjectTypeEntity

@pytest.fixture
def mock_types_repository():
    return MagicMock()

@pytest.fixture
def mock_project_type_repository():
    return MagicMock()

@pytest.fixture
def project_type_entity():
    from datetime import datetime
    return ProjectTypeEntity(types_id=1, project_id=1, created_at=datetime.now())

def test_delete_type_success(mock_types_repository):
    use_case = DeleteType(mock_types_repository)
    use_case.delete("Test Type")
    
    mock_types_repository.delete.assert_called_once_with(name="Test Type")

def test_delete_type_repository_error(mock_types_repository):
    mock_types_repository.delete.side_effect = Exception("Repository error")
    
    use_case = DeleteType(mock_types_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete("Test Type")

def test_find_type_from_project_success(mock_project_type_repository, project_type_entity):
    mock_project_type_repository.select_all_from_project.return_value = [project_type_entity]
    
    use_case = FindTypeFromProject(mock_project_type_repository)
    result = use_case.find(1)
    
    mock_project_type_repository.select_all_from_project.assert_called_once_with(project_id=1)
    assert result == [project_type_entity]

def test_find_type_from_project_empty_list(mock_project_type_repository):
    mock_project_type_repository.select_all_from_project.return_value = []
    
    use_case = FindTypeFromProject(mock_project_type_repository)
    result = use_case.find(1)
    
    mock_project_type_repository.select_all_from_project.assert_called_once_with(project_id=1)
    assert result == []

def test_find_type_from_project_repository_error(mock_project_type_repository):
    mock_project_type_repository.select_all_from_project.side_effect = Exception("Repository error")
    
    use_case = FindTypeFromProject(mock_project_type_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.find(1)

def test_delete_type_from_project_success(mock_project_type_repository):
    use_case = DeleteTypeFromProject(mock_project_type_repository)
    use_case.delete(1)
    
    mock_project_type_repository.delete_all_from_project.assert_called_once_with(project_id=1)

def test_delete_type_from_project_repository_error(mock_project_type_repository):
    mock_project_type_repository.delete_all_from_project.side_effect = Exception("Repository error")
    
    use_case = DeleteTypeFromProject(mock_project_type_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1)

def test_create_project_type_success(mock_project_type_repository):
    use_case = CreateProjectType(mock_project_type_repository)
    use_case.create(1, 2)
    
    mock_project_type_repository.insert.assert_called_once_with(project_id=1, type_id=2)

def test_create_project_type_repository_error(mock_project_type_repository):
    mock_project_type_repository.insert.side_effect = Exception("Repository error")
    
    use_case = CreateProjectType(mock_project_type_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.create(1, 2) 