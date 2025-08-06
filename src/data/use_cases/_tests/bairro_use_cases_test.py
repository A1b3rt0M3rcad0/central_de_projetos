#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.create_bairro import CreateBairro
from src.data.use_cases.find_bairro_by_name import FindBairroByName
from src.data.use_cases.update_bairro_name import UpdateBairroName
from src.data.use_cases.delete_bairro import DeleteBairro
from src.data.use_cases.find_bairro_by_id import FindBairrobyId
from src.data.use_cases.count_bairros import CountBairros
from src.data.use_cases.find_all_bairro import FindAllBairro
from src.domain.entities.bairro import BairroEntity
from src.errors.repository.not_exists_error.bairro_not_exists import BairroNotExists
from src.errors.repository.already_exists_error.bairro_already_exists import BairroAlreadyExists

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def bairro_entity():
    from datetime import datetime
    return BairroEntity(
        bairro_id=1,
        name="Centro",
        created_at=datetime.now()
    )

def test_create_bairro_success(mock_repository):
    """Testa criação bem-sucedida de bairro"""
    use_case = CreateBairro(mock_repository)
    
    use_case.create("Novo Bairro")
    
    mock_repository.insert.assert_called_once_with(name="Novo Bairro")

def test_create_bairro_repository_error(mock_repository):
    """Testa criação de bairro quando repositório lança exceção"""
    mock_repository.insert.side_effect = BairroAlreadyExists("Bairro já existe")
    use_case = CreateBairro(mock_repository)
    
    with pytest.raises(BairroAlreadyExists):
        use_case.create("Bairro Existente")

def test_find_bairro_by_name_success(mock_repository, bairro_entity):
    """Testa busca de bairro por nome com sucesso"""
    mock_repository.find_by_name.return_value = bairro_entity
    use_case = FindBairroByName(mock_repository)
    
    result = use_case.find("Centro")
    
    mock_repository.find_by_name.assert_called_once_with(name="Centro")
    assert result == bairro_entity

def test_find_bairro_by_name_not_found(mock_repository):
    """Testa busca de bairro por nome quando não encontrado"""
    mock_repository.find_by_name.side_effect = BairroNotExists("Bairro não encontrado")
    use_case = FindBairroByName(mock_repository)
    
    with pytest.raises(BairroNotExists):
        use_case.find("Bairro Inexistente")

def test_update_bairro_name_success(mock_repository):
    """Testa atualização de nome de bairro com sucesso"""
    use_case = UpdateBairroName(mock_repository)
    
    use_case.update("Nome Antigo", "Novo Nome")
    
    mock_repository.update.assert_called_once_with(name="Nome Antigo", new_name="Novo Nome")

def test_update_bairro_name_repository_error(mock_repository):
    """Testa atualização de nome quando repositório lança exceção"""
    mock_repository.update.side_effect = BairroNotExists("Bairro não encontrado")
    use_case = UpdateBairroName(mock_repository)
    
    with pytest.raises(BairroNotExists):
        use_case.update(999, "Novo Nome")

def test_delete_bairro_success(mock_repository):
    """Testa exclusão de bairro com sucesso"""
    use_case = DeleteBairro(mock_repository)
    
    use_case.delete("Nome do Bairro")
    
    mock_repository.delete.assert_called_once_with(name="Nome do Bairro")

def test_delete_bairro_repository_error(mock_repository):
    """Testa exclusão de bairro quando repositório lança exceção"""
    mock_repository.delete.side_effect = BairroNotExists("Bairro não encontrado")
    use_case = DeleteBairro(mock_repository)
    
    with pytest.raises(BairroNotExists):
        use_case.delete(999)

def test_find_bairro_by_id_success(mock_repository, bairro_entity):
    """Testa busca de bairro por ID com sucesso"""
    mock_repository.find_by_id.return_value = bairro_entity
    use_case = FindBairrobyId(mock_repository)
    
    result = use_case.find(1)
    
    mock_repository.find_by_id.assert_called_once_with(bairro_id=1)
    assert result == bairro_entity

def test_find_bairro_by_id_not_found(mock_repository):
    """Testa busca de bairro por ID quando não encontrado"""
    mock_repository.find_by_id.side_effect = BairroNotExists("Bairro não encontrado")
    use_case = FindBairrobyId(mock_repository)
    
    with pytest.raises(BairroNotExists):
        use_case.find(999)

def test_count_bairros_success(mock_repository):
    """Testa contagem de bairros com sucesso"""
    mock_repository.count_bairros.return_value = {"count": 5}
    use_case = CountBairros(mock_repository)
    
    result = use_case.count()
    
    mock_repository.count_bairros.assert_called_once()
    assert result == {"count": 5}

def test_find_all_bairro_success(mock_repository):
    """Testa busca de todos os bairros com sucesso"""
    from datetime import datetime
    bairros = [
        BairroEntity(bairro_id=1, name="Centro", created_at=datetime.now()),
        BairroEntity(bairro_id=2, name="Vila", created_at=datetime.now())
    ]
    mock_repository.find_all.return_value = bairros
    use_case = FindAllBairro(mock_repository)
    
    result = use_case.find()
    
    mock_repository.find_all.assert_called_once()
    assert result == bairros 