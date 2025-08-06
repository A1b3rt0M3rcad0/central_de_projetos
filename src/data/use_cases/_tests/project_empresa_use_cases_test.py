#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.find_project_empresa import FindProjectEmpresa
from src.data.use_cases.create_project_empresa import CreateProjectEmpresa
from src.data.use_cases.delete_project_empresa import DeleteProjectEmpresa
from src.data.use_cases.delete_empresa_from_project import DeleteEmpresaFromProject
from src.domain.entities.project_empresa import ProjectEmpresaEntity

@pytest.fixture
def mock_project_empresa_repository():
    return MagicMock()

@pytest.fixture
def project_empresa_entity():
    from datetime import datetime
    return ProjectEmpresaEntity(
        project_id=1,
        empresa_id=1,
        created_at=datetime.now()
    )

def test_find_project_empresa_success(mock_project_empresa_repository, project_empresa_entity):
    mock_project_empresa_repository.find.return_value = project_empresa_entity
    
    use_case = FindProjectEmpresa(mock_project_empresa_repository)
    result = use_case.find(1, 1)
    
    mock_project_empresa_repository.find.assert_called_once_with(empresa_id=1, project_id=1)
    assert result == project_empresa_entity

def test_find_project_empresa_repository_error(mock_project_empresa_repository):
    mock_project_empresa_repository.find.side_effect = Exception("Repository error")
    
    use_case = FindProjectEmpresa(mock_project_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.find(1, 1)

def test_create_project_empresa_success(mock_project_empresa_repository):
    use_case = CreateProjectEmpresa(mock_project_empresa_repository)
    use_case.create(1, 1)
    
    mock_project_empresa_repository.insert.assert_called_once_with(empresa_id=1, project_id=1)

def test_create_project_empresa_repository_error(mock_project_empresa_repository):
    mock_project_empresa_repository.insert.side_effect = Exception("Repository error")
    
    use_case = CreateProjectEmpresa(mock_project_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.create(1, 1)

def test_delete_project_empresa_success(mock_project_empresa_repository):
    use_case = DeleteProjectEmpresa(mock_project_empresa_repository)
    use_case.delete(1, 1)
    
    mock_project_empresa_repository.delete.assert_called_once_with(empresa_id=1, project_id=1)

def test_delete_project_empresa_repository_error(mock_project_empresa_repository):
    mock_project_empresa_repository.delete.side_effect = Exception("Repository error")
    
    use_case = DeleteProjectEmpresa(mock_project_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1, 1)

def test_delete_empresa_from_project_success(mock_project_empresa_repository):
    use_case = DeleteEmpresaFromProject(mock_project_empresa_repository)
    use_case.delete(1)
    
    mock_project_empresa_repository.delete_all_from_project.assert_called_once_with(project_id=1)

def test_delete_empresa_from_project_repository_error(mock_project_empresa_repository):
    mock_project_empresa_repository.delete_all_from_project.side_effect = Exception("Repository error")
    
    use_case = DeleteEmpresaFromProject(mock_project_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1) 