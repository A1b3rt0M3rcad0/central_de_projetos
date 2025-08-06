#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.find_project_bairro import FindProjectBairro
from src.data.use_cases.create_project_bairro import CreateProjectBairro
from src.data.use_cases.delete_project_bairro import DeleteProjectBairro
from src.data.use_cases.delete_bairro_from_project import DeleteBairroFromProject
from src.data.use_cases.update_bairro_from_project import UpdateBairroFromProject
from src.domain.entities.project_bairro import ProjectBairroEntity

@pytest.fixture
def mock_project_bairro_repository():
    return MagicMock()

@pytest.fixture
def project_bairro_entity():
    from datetime import datetime
    return ProjectBairroEntity(
        project_id=1,
        bairro_id=1,
        created_at=datetime.now()
    )

def test_find_project_bairro_success(mock_project_bairro_repository, project_bairro_entity):
    mock_project_bairro_repository.find.return_value = project_bairro_entity
    
    use_case = FindProjectBairro(mock_project_bairro_repository)
    result = use_case.find(1, 1)
    
    mock_project_bairro_repository.find.assert_called_once_with(project_id=1, bairro_id=1)
    assert result == project_bairro_entity

def test_find_project_bairro_repository_error(mock_project_bairro_repository):
    mock_project_bairro_repository.find.side_effect = Exception("Repository error")
    
    use_case = FindProjectBairro(mock_project_bairro_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.find(1, 1)

def test_create_project_bairro_success(mock_project_bairro_repository):
    use_case = CreateProjectBairro(mock_project_bairro_repository)
    use_case.create(1, 1)
    
    mock_project_bairro_repository.insert.assert_called_once_with(bairro_id=1, project_id=1)

def test_create_project_bairro_repository_error(mock_project_bairro_repository):
    mock_project_bairro_repository.insert.side_effect = Exception("Repository error")
    
    use_case = CreateProjectBairro(mock_project_bairro_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.create(1, 1)

def test_delete_project_bairro_success(mock_project_bairro_repository):
    use_case = DeleteProjectBairro(mock_project_bairro_repository)
    use_case.delete(1, 1)
    
    mock_project_bairro_repository.delete.assert_called_once_with(project_id=1, bairro_id=1)

def test_delete_project_bairro_repository_error(mock_project_bairro_repository):
    mock_project_bairro_repository.delete.side_effect = Exception("Repository error")
    
    use_case = DeleteProjectBairro(mock_project_bairro_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1, 1)

def test_delete_bairro_from_project_success(mock_project_bairro_repository):
    use_case = DeleteBairroFromProject(mock_project_bairro_repository)
    use_case.delete(1)
    
    mock_project_bairro_repository.delete_all_from_project.assert_called_once_with(project_id=1)

def test_delete_bairro_from_project_repository_error(mock_project_bairro_repository):
    mock_project_bairro_repository.delete_all_from_project.side_effect = Exception("Repository error")
    
    use_case = DeleteBairroFromProject(mock_project_bairro_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1)

def test_update_bairro_from_project_success(mock_project_bairro_repository):
    use_case = UpdateBairroFromProject(mock_project_bairro_repository)
    use_case.update(1, 1, 2)
    
    mock_project_bairro_repository.update_bairro.assert_called_once_with(
        project_id=1, 
        bairro_id=1, 
        new_bairro_id=2
    )

def test_update_bairro_from_project_repository_error(mock_project_bairro_repository):
    mock_project_bairro_repository.update_bairro.side_effect = Exception("Repository error")
    
    use_case = UpdateBairroFromProject(mock_project_bairro_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.update(1, 1, 2) 