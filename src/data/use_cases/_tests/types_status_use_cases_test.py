#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.find_all_types import FindAllTypes
from src.data.use_cases.find_all_status import FindAllStatus
from src.data.use_cases.create_type import CreateType
from src.data.use_cases.update_type import UpdateType
from src.domain.entities.types import TypesEntity
from src.domain.entities.status import StatusEntity

@pytest.fixture
def mock_types_repository():
    return MagicMock()

@pytest.fixture
def mock_status_repository():
    return MagicMock()

@pytest.fixture
def types_entity():
    from datetime import datetime
    return TypesEntity(
        types_id=1,
        name="Tipo Teste",
        created_at=datetime.now()
    )

@pytest.fixture
def status_entity():
    from datetime import datetime
    return StatusEntity(
        status_id=1,
        description="Status Teste",
        created_at=datetime.now()
    )

# Testes para FindAllTypes
def test_find_all_types_success(mock_types_repository, types_entity):
    """Testa busca de todos os tipos com sucesso"""
    mock_types_repository.find_all.return_value = [types_entity]
    use_case = FindAllTypes(mock_types_repository)
    
    result = use_case.find()
    
    mock_types_repository.find_all.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], TypesEntity)

def test_find_all_types_empty_list(mock_types_repository):
    """Testa busca de todos os tipos quando lista está vazia"""
    mock_types_repository.find_all.return_value = []
    use_case = FindAllTypes(mock_types_repository)
    
    result = use_case.find()
    
    mock_types_repository.find_all.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 0

def test_find_all_types_repository_error(mock_types_repository):
    """Testa busca de todos os tipos quando repositório lança exceção"""
    mock_types_repository.find_all.side_effect = Exception("Erro no repositório")
    use_case = FindAllTypes(mock_types_repository)
    
    with pytest.raises(Exception):
        use_case.find()

# Testes para FindAllStatus
def test_find_all_status_success(mock_status_repository, status_entity):
    """Testa busca de todos os status com sucesso"""
    mock_status_repository.find_all.return_value = [status_entity]
    use_case = FindAllStatus(mock_status_repository)
    
    result = use_case.find()
    
    mock_status_repository.find_all.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], StatusEntity)

def test_find_all_status_empty_list(mock_status_repository):
    """Testa busca de todos os status quando lista está vazia"""
    mock_status_repository.find_all.return_value = []
    use_case = FindAllStatus(mock_status_repository)
    
    result = use_case.find()
    
    mock_status_repository.find_all.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 0

def test_find_all_status_repository_error(mock_status_repository):
    """Testa busca de todos os status quando repositório lança exceção"""
    mock_status_repository.find_all.side_effect = Exception("Erro no repositório")
    use_case = FindAllStatus(mock_status_repository)
    
    with pytest.raises(Exception):
        use_case.find()

# Testes para CreateType
def test_create_type_success(mock_types_repository):
    """Testa criação de tipo com sucesso"""
    use_case = CreateType(mock_types_repository)
    
    use_case.create(name="Novo Tipo")
    
    mock_types_repository.insert.assert_called_once_with(name="Novo Tipo")

def test_create_type_repository_error(mock_types_repository):
    """Testa criação de tipo quando repositório lança exceção"""
    mock_types_repository.insert.side_effect = Exception("Erro no repositório")
    use_case = CreateType(mock_types_repository)
    
    with pytest.raises(Exception):
        use_case.create(name="Novo Tipo")

def test_create_type_empty_name(mock_types_repository):
    """Testa criação de tipo com nome vazio"""
    use_case = CreateType(mock_types_repository)
    
    use_case.create(name="")
    
    mock_types_repository.insert.assert_called_once_with(name="")

# Testes para UpdateType
def test_update_type_success(mock_types_repository):
    """Testa atualização de tipo com sucesso"""
    use_case = UpdateType(mock_types_repository)
    
    use_case.update(name="Tipo Antigo", new_name="Tipo Novo")
    
    mock_types_repository.update.assert_called_once_with(
        name="Tipo Antigo",
        new_name="Tipo Novo"
    )

def test_update_type_repository_error(mock_types_repository):
    """Testa atualização de tipo quando repositório lança exceção"""
    mock_types_repository.update.side_effect = Exception("Erro no repositório")
    use_case = UpdateType(mock_types_repository)
    
    with pytest.raises(Exception):
        use_case.update(name="Tipo Antigo", new_name="Tipo Novo")

def test_update_type_same_name(mock_types_repository):
    """Testa atualização de tipo com o mesmo nome"""
    use_case = UpdateType(mock_types_repository)
    
    use_case.update(name="Mesmo Nome", new_name="Mesmo Nome")
    
    mock_types_repository.update.assert_called_once_with(
        name="Mesmo Nome",
        new_name="Mesmo Nome"
    ) 