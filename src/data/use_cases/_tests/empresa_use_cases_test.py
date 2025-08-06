#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.create_empresa import CreateEmpresa
from src.data.use_cases.update_empresa import UpdateEmpresa
from src.data.use_cases.delete_empresa import DeleteEmpresa
from src.data.use_cases.find_empresa_by_exact_name import FindEmpresaByExactName
from src.domain.entities.empresa import EmpresaEntity

@pytest.fixture
def mock_empresa_repository():
    return MagicMock()

@pytest.fixture
def empresa_entity():
    from datetime import datetime
    return EmpresaEntity(empresa_id=1, name="Test Company", created_at=datetime.now())

def test_create_empresa_success(mock_empresa_repository):
    use_case = CreateEmpresa(mock_empresa_repository)
    use_case.create("Test Company")
    
    mock_empresa_repository.insert.assert_called_once_with(name="Test Company")

def test_create_empresa_repository_error(mock_empresa_repository):
    mock_empresa_repository.insert.side_effect = Exception("Repository error")
    
    use_case = CreateEmpresa(mock_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.create("Test Company")

def test_update_empresa_success(mock_empresa_repository):
    use_case = UpdateEmpresa(mock_empresa_repository)
    use_case.update("Old Name", "New Name")
    
    mock_empresa_repository.update.assert_called_once_with(name="Old Name", new_name="New Name")

def test_update_empresa_repository_error(mock_empresa_repository):
    mock_empresa_repository.update.side_effect = Exception("Repository error")
    
    use_case = UpdateEmpresa(mock_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.update("Old Name", "New Name")

def test_delete_empresa_success(mock_empresa_repository):
    use_case = DeleteEmpresa(mock_empresa_repository)
    use_case.delete("Test Company")
    
    mock_empresa_repository.delete.assert_called_once_with(name="Test Company")

def test_delete_empresa_repository_error(mock_empresa_repository):
    mock_empresa_repository.delete.side_effect = Exception("Repository error")
    
    use_case = DeleteEmpresa(mock_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete("Test Company")

def test_find_empresa_by_exact_name_success(mock_empresa_repository, empresa_entity):
    mock_empresa_repository.find_by_name.return_value = empresa_entity
    
    use_case = FindEmpresaByExactName(mock_empresa_repository)
    result = use_case.find("Test Company")
    
    mock_empresa_repository.find_by_name.assert_called_once_with(name="Test Company")
    assert result == empresa_entity

def test_find_empresa_by_exact_name_repository_error(mock_empresa_repository):
    mock_empresa_repository.find_by_name.side_effect = Exception("Repository error")
    
    use_case = FindEmpresaByExactName(mock_empresa_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.find("Test Company") 