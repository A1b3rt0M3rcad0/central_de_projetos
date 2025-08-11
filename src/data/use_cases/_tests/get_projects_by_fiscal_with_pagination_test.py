#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.get_projects_by_fiscal_with_pagination import GetProjectsByFiscalWithPagination
from src.domain.entities.project_fiscal import ProjectFiscalEntity
from datetime import datetime, timezone

@pytest.fixture
def mock_project_fiscal_repository():
    return MagicMock()

@pytest.fixture
def project_fiscal_entity():
    return ProjectFiscalEntity(
        project_id=1,
        fiscal_id=1,
        created_at=datetime.now(timezone.utc)
    )

def test_get_projects_by_fiscal_with_pagination_success(mock_project_fiscal_repository, project_fiscal_entity):
    """Testa busca de projetos por fiscal com paginação com sucesso"""
    expected_result = {
        "page": 1,
        "page_size": 10,
        "total_items": 25,
        "total_pages": 3,
        "projects": [project_fiscal_entity]
    }
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.return_value = expected_result
    use_case = GetProjectsByFiscalWithPagination(mock_project_fiscal_repository)
    
    result = use_case.get(fiscal_id=1, page=1, page_size=10)
    
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.assert_called_once_with(
        fiscal_id=1, page=1, page_size=10
    )
    assert isinstance(result, dict)
    assert result == expected_result
    assert result["page"] == 1
    assert result["page_size"] == 10
    assert result["total_items"] == 25
    assert result["total_pages"] == 3
    assert len(result["projects"]) == 1

def test_get_projects_by_fiscal_with_pagination_default_page_size(mock_project_fiscal_repository, project_fiscal_entity):
    """Testa busca de projetos por fiscal com tamanho de página padrão"""
    expected_result = {
        "page": 2,
        "page_size": 10,
        "total_items": 15,
        "total_pages": 2,
        "projects": [project_fiscal_entity]
    }
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.return_value = expected_result
    use_case = GetProjectsByFiscalWithPagination(mock_project_fiscal_repository)
    
    result = use_case.get(fiscal_id=1, page=2)
    
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.assert_called_once_with(
        fiscal_id=1, page=2, page_size=10
    )
    assert isinstance(result, dict)
    assert result == expected_result
    assert result["page"] == 2
    assert result["page_size"] == 10

def test_get_projects_by_fiscal_with_pagination_empty_result(mock_project_fiscal_repository):
    """Testa busca de projetos por fiscal quando não há projetos"""
    expected_result = {
        "page": 1,
        "page_size": 10,
        "total_items": 0,
        "total_pages": 0,
        "projects": []
    }
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.return_value = expected_result
    use_case = GetProjectsByFiscalWithPagination(mock_project_fiscal_repository)
    
    result = use_case.get(fiscal_id=1, page=1, page_size=10)
    
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.assert_called_once_with(
        fiscal_id=1, page=1, page_size=10
    )
    assert isinstance(result, dict)
    assert result == expected_result
    assert result["total_items"] == 0
    assert result["total_pages"] == 0
    assert len(result["projects"]) == 0

def test_get_projects_by_fiscal_with_pagination_repository_error(mock_project_fiscal_repository):
    """Testa busca de projetos por fiscal quando repositório lança exceção"""
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.side_effect = Exception("Erro no repositório")
    use_case = GetProjectsByFiscalWithPagination(mock_project_fiscal_repository)
    
    with pytest.raises(Exception):
        use_case.get(fiscal_id=1, page=1, page_size=10)

def test_get_projects_by_fiscal_with_pagination_multiple_pages(mock_project_fiscal_repository):
    """Testa busca de projetos por fiscal com múltiplas páginas"""
    # Simular 50 projetos, 10 por página = 5 páginas
    projects = [
        ProjectFiscalEntity(project_id=i, fiscal_id=1, created_at=datetime.now(timezone.utc))
        for i in range(1, 11)  # 10 projetos na página 1
    ]
    
    expected_result = {
        "page": 1,
        "page_size": 10,
        "total_items": 50,
        "total_pages": 5,
        "projects": projects
    }
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.return_value = expected_result
    use_case = GetProjectsByFiscalWithPagination(mock_project_fiscal_repository)
    
    result = use_case.get(fiscal_id=1, page=1, page_size=10)
    
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.assert_called_once_with(
        fiscal_id=1, page=1, page_size=10
    )
    assert isinstance(result, dict)
    assert result == expected_result
    assert result["page"] == 1
    assert result["page_size"] == 10
    assert result["total_items"] == 50
    assert result["total_pages"] == 5
    assert len(result["projects"]) == 10

def test_get_projects_by_fiscal_with_pagination_custom_page_size(mock_project_fiscal_repository, project_fiscal_entity):
    """Testa busca de projetos por fiscal com tamanho de página personalizado"""
    expected_result = {
        "page": 1,
        "page_size": 5,
        "total_items": 12,
        "total_pages": 3,
        "projects": [project_fiscal_entity]
    }
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.return_value = expected_result
    use_case = GetProjectsByFiscalWithPagination(mock_project_fiscal_repository)
    
    result = use_case.get(fiscal_id=1, page=1, page_size=5)
    
    mock_project_fiscal_repository.get_projects_by_fiscal_with_pagination.assert_called_once_with(
        fiscal_id=1, page=1, page_size=5
    )
    assert isinstance(result, dict)
    assert result == expected_result
    assert result["page"] == 1
    assert result["page_size"] == 5
    assert result["total_items"] == 12
    assert result["total_pages"] == 3 