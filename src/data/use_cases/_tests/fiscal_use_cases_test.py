#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.find_all_fiscal import FindAllFiscal
from src.data.use_cases.find_fiscal_by_id import FindFiscalById
from src.data.use_cases.count_fiscals import CountFiscals
from src.domain.entities.fiscal import FiscalEntity

@pytest.fixture
def mock_fiscal_repository():
    return MagicMock()

@pytest.fixture
def fiscal_entity():
    from datetime import datetime
    from src.domain.value_objects.email import Email
    return FiscalEntity(
        fiscal_id=1,
        name="Fiscal Teste",
        created_at=datetime.now(),
        password=b"hashed_password",
        salt=b"salt_value",
        email=Email("fiscal@example.com")
    )

# Testes para FindAllFiscal
def test_find_all_fiscal_success(mock_fiscal_repository, fiscal_entity):
    """Testa busca de todos os fiscais com sucesso"""
    mock_fiscal_repository.find_all.return_value = [fiscal_entity]
    use_case = FindAllFiscal(mock_fiscal_repository)
    
    result = use_case.find()
    
    mock_fiscal_repository.find_all.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], FiscalEntity)

def test_find_all_fiscal_empty_list(mock_fiscal_repository):
    """Testa busca de todos os fiscais quando lista está vazia"""
    mock_fiscal_repository.find_all.return_value = []
    use_case = FindAllFiscal(mock_fiscal_repository)
    
    result = use_case.find()
    
    mock_fiscal_repository.find_all.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 0

def test_find_all_fiscal_repository_error(mock_fiscal_repository):
    """Testa busca de todos os fiscais quando repositório lança exceção"""
    mock_fiscal_repository.find_all.side_effect = Exception("Erro no repositório")
    use_case = FindAllFiscal(mock_fiscal_repository)
    
    with pytest.raises(Exception):
        use_case.find()

# Testes para FindFiscalById
def test_find_fiscal_by_id_success(mock_fiscal_repository, fiscal_entity):
    """Testa busca de fiscal por ID com sucesso"""
    mock_fiscal_repository.find_by_id.return_value = fiscal_entity
    use_case = FindFiscalById(mock_fiscal_repository)
    
    result = use_case.find(fiscal_id=1)
    
    mock_fiscal_repository.find_by_id.assert_called_once_with(fiscal_id=1)
    assert isinstance(result, FiscalEntity)
    assert result.fiscal_id == 1

def test_find_fiscal_by_id_not_found(mock_fiscal_repository):
    """Testa busca de fiscal por ID quando não encontrado"""
    mock_fiscal_repository.find_by_id.side_effect = AttributeError("Fiscal não encontrado")
    use_case = FindFiscalById(mock_fiscal_repository)
    
    with pytest.raises(AttributeError):
        use_case.find(fiscal_id=999)

def test_find_fiscal_by_id_repository_error(mock_fiscal_repository):
    """Testa busca de fiscal por ID quando repositório lança exceção"""
    mock_fiscal_repository.find_by_id.side_effect = Exception("Erro no repositório")
    use_case = FindFiscalById(mock_fiscal_repository)
    
    with pytest.raises(Exception):
        use_case.find(fiscal_id=1)

# Testes para CountFiscals
def test_count_fiscals_success(mock_fiscal_repository):
    """Testa contagem de fiscais com sucesso"""
    expected_count = {"total": 5, "active": 3, "inactive": 2}
    mock_fiscal_repository.count_fiscals.return_value = expected_count
    use_case = CountFiscals(mock_fiscal_repository)
    
    result = use_case.count()
    
    mock_fiscal_repository.count_fiscals.assert_called_once()
    assert isinstance(result, dict)
    assert result == expected_count
    assert result["total"] == 5
    assert result["active"] == 3
    assert result["inactive"] == 2

def test_count_fiscals_zero_count(mock_fiscal_repository):
    """Testa contagem de fiscais quando não há fiscais"""
    expected_count = {"total": 0, "active": 0, "inactive": 0}
    mock_fiscal_repository.count_fiscals.return_value = expected_count
    use_case = CountFiscals(mock_fiscal_repository)
    
    result = use_case.count()
    
    mock_fiscal_repository.count_fiscals.assert_called_once()
    assert isinstance(result, dict)
    assert result == expected_count
    assert result["total"] == 0

def test_count_fiscals_repository_error(mock_fiscal_repository):
    """Testa contagem de fiscais quando repositório lança exceção"""
    mock_fiscal_repository.count_fiscals.side_effect = Exception("Erro no repositório")
    use_case = CountFiscals(mock_fiscal_repository)
    
    with pytest.raises(Exception):
        use_case.count() 