#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.count_projects import CountProjects
from src.data.use_cases.count_empresas import CountEmpresas
from src.data.use_cases.count_bairros import CountBairros
from src.data.use_cases.get_projects_with_pagination import GetProjectsWithPagination
from src.domain.entities.project import ProjectEntity

@pytest.fixture
def mock_project_repository():
    return MagicMock()

@pytest.fixture
def mock_empresa_repository():
    return MagicMock()

@pytest.fixture
def mock_bairro_repository():
    return MagicMock()

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

# Testes para CountProjects
def test_count_projects_success(mock_project_repository):
    """Testa contagem de projetos com sucesso"""
    expected_count = {"total": 10, "active": 7, "inactive": 3}
    mock_project_repository.count_projects.return_value = expected_count
    use_case = CountProjects(mock_project_repository)
    
    result = use_case.count()
    
    mock_project_repository.count_projects.assert_called_once()
    assert isinstance(result, dict)
    assert result == expected_count
    assert result["total"] == 10
    assert result["active"] == 7
    assert result["inactive"] == 3

def test_count_projects_zero_count(mock_project_repository):
    """Testa contagem de projetos quando não há projetos"""
    expected_count = {"total": 0, "active": 0, "inactive": 0}
    mock_project_repository.count_projects.return_value = expected_count
    use_case = CountProjects(mock_project_repository)
    
    result = use_case.count()
    
    mock_project_repository.count_projects.assert_called_once()
    assert isinstance(result, dict)
    assert result == expected_count
    assert result["total"] == 0

def test_count_projects_repository_error(mock_project_repository):
    """Testa contagem de projetos quando repositório lança exceção"""
    mock_project_repository.count_projects.side_effect = Exception("Erro no repositório")
    use_case = CountProjects(mock_project_repository)
    
    with pytest.raises(Exception):
        use_case.count()

# Testes para CountEmpresas
def test_count_empresas_success(mock_empresa_repository):
    """Testa contagem de empresas com sucesso"""
    expected_count = {"total": 5, "active": 4, "inactive": 1}
    mock_empresa_repository.count_empresas.return_value = expected_count
    use_case = CountEmpresas(mock_empresa_repository)
    
    result = use_case.count()
    
    mock_empresa_repository.count_empresas.assert_called_once()
    assert isinstance(result, dict)
    assert result == expected_count
    assert result["total"] == 5
    assert result["active"] == 4
    assert result["inactive"] == 1

def test_count_empresas_zero_count(mock_empresa_repository):
    """Testa contagem de empresas quando não há empresas"""
    expected_count = {"total": 0, "active": 0, "inactive": 0}
    mock_empresa_repository.count_empresas.return_value = expected_count
    use_case = CountEmpresas(mock_empresa_repository)
    
    result = use_case.count()
    
    mock_empresa_repository.count_empresas.assert_called_once()
    assert isinstance(result, dict)
    assert result == expected_count
    assert result["total"] == 0

def test_count_empresas_repository_error(mock_empresa_repository):
    """Testa contagem de empresas quando repositório lança exceção"""
    mock_empresa_repository.count_empresas.side_effect = Exception("Erro no repositório")
    use_case = CountEmpresas(mock_empresa_repository)
    
    with pytest.raises(Exception):
        use_case.count()

# Testes para CountBairros
def test_count_bairros_success(mock_bairro_repository):
    """Testa contagem de bairros com sucesso"""
    expected_count = {"total": 8, "active": 6, "inactive": 2}
    mock_bairro_repository.count_bairros.return_value = expected_count
    use_case = CountBairros(mock_bairro_repository)
    
    result = use_case.count()
    
    mock_bairro_repository.count_bairros.assert_called_once()
    assert isinstance(result, dict)
    assert result == expected_count
    assert result["total"] == 8
    assert result["active"] == 6
    assert result["inactive"] == 2

def test_count_bairros_zero_count(mock_bairro_repository):
    """Testa contagem de bairros quando não há bairros"""
    expected_count = {"total": 0, "active": 0, "inactive": 0}
    mock_bairro_repository.count_bairros.return_value = expected_count
    use_case = CountBairros(mock_bairro_repository)
    
    result = use_case.count()
    
    mock_bairro_repository.count_bairros.assert_called_once()
    assert isinstance(result, dict)
    assert result == expected_count
    assert result["total"] == 0

def test_count_bairros_repository_error(mock_bairro_repository):
    """Testa contagem de bairros quando repositório lança exceção"""
    mock_bairro_repository.count_bairros.side_effect = Exception("Erro no repositório")
    use_case = CountBairros(mock_bairro_repository)
    
    with pytest.raises(Exception):
        use_case.count()

# Testes para GetProjectsWithPagination
def test_get_projects_with_pagination_success(mock_project_repository, project_entity):
    """Testa busca de projetos com paginação com sucesso"""
    expected_result = {
        "total": 1,
        "projects": [project_entity]
    }
    mock_project_repository.get_projects_with_pagination.return_value = expected_result
    use_case = GetProjectsWithPagination(mock_project_repository)
    
    result = use_case.get(page=1, page_size=10)
    
    mock_project_repository.get_projects_with_pagination.assert_called_once_with(page=1, page_size=10)
    assert isinstance(result, dict)
    assert result == expected_result
    assert result["total"] == 1
    assert len(result["projects"]) == 1

def test_get_projects_with_pagination_empty_page(mock_project_repository):
    """Testa busca de projetos com paginação quando página está vazia"""
    expected_result = {
        "total": 0,
        "projects": []
    }
    mock_project_repository.get_projects_with_pagination.return_value = expected_result
    use_case = GetProjectsWithPagination(mock_project_repository)
    
    result = use_case.get(page=5, page_size=10)
    
    mock_project_repository.get_projects_with_pagination.assert_called_once_with(page=5, page_size=10)
    assert isinstance(result, dict)
    assert result == expected_result
    assert result["total"] == 0
    assert len(result["projects"]) == 0

def test_get_projects_with_pagination_default_page_size(mock_project_repository, project_entity):
    """Testa busca de projetos com paginação usando tamanho de página padrão"""
    expected_result = {
        "total": 1,
        "projects": [project_entity]
    }
    mock_project_repository.get_projects_with_pagination.return_value = expected_result
    use_case = GetProjectsWithPagination(mock_project_repository)
    
    result = use_case.get(page=1)
    
    mock_project_repository.get_projects_with_pagination.assert_called_once_with(page=1, page_size=10)
    assert isinstance(result, dict)
    assert result == expected_result

def test_get_projects_with_pagination_repository_error(mock_project_repository):
    """Testa busca de projetos com paginação quando repositório lança exceção"""
    mock_project_repository.get_projects_with_pagination.side_effect = Exception("Erro no repositório")
    use_case = GetProjectsWithPagination(mock_project_repository)
    
    with pytest.raises(Exception):
        use_case.get(page=1, page_size=10) 