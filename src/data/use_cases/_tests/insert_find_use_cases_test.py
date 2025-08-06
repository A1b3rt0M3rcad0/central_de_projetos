#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.insert_all_fiscal_from_user import InsertAllFiscalFromFiscalUseCase
from src.data.use_cases.find_bairro_by_id import FindBairrobyId
from src.data.use_cases.find_type_by_exact_name import FindTypebyExactName
from src.domain.entities.bairro import BairroEntity
from src.domain.entities.types import TypesEntity
from src.security.value_objects.hashed_password import HashedPassword

@pytest.fixture
def mock_fiscal_repository():
    return MagicMock()

@pytest.fixture
def mock_bairro_repository():
    return MagicMock()

@pytest.fixture
def mock_types_repository():
    return MagicMock()

@pytest.fixture
def bairro_entity():
    from datetime import datetime
    return BairroEntity(
        bairro_id=1,
        name="Bairro Teste",
        created_at=datetime.now()
    )

@pytest.fixture
def types_entity():
    from datetime import datetime
    return TypesEntity(
        types_id=1,
        name="Tipo Teste",
        created_at=datetime.now()
    )

# Testes para InsertAllFiscalFromFiscalUseCase
def test_insert_all_fiscal_from_user_success(mock_fiscal_repository):
    """Testa inserção de fiscal com sucesso"""
    from src.domain.value_objects.email import Email
    from src.security.cryptography.utils.salt import Salt
    from src.security.cryptography.blowfish_crypt import BlowfishCrypt
    
    # Criar um hashed password válido
    password = HashedPassword(
        password="Password123",
        cryptography=BlowfishCrypt(),
        salt=Salt(b"salt_value")
    )
    
    use_case = InsertAllFiscalFromFiscalUseCase(mock_fiscal_repository)
    
    use_case.execute(
        name="Fiscal Teste",
        email=Email("fiscal@example.com"),
        password=password,
        phone="11999999999"
    )
    
    mock_fiscal_repository.insert_all_from_fiscal.assert_called_once()
    call_args = mock_fiscal_repository.insert_all_from_fiscal.call_args
    assert call_args[0][0] == "Fiscal Teste"  # Primeiro argumento posicional
    assert call_args[0][1].email == "fiscal@example.com"  # Segundo argumento posicional
    assert call_args[0][3] == "11999999999"  # Quarto argumento posicional

def test_insert_all_fiscal_from_user_repository_error(mock_fiscal_repository):
    """Testa inserção de fiscal quando repositório lança exceção"""
    from src.domain.value_objects.email import Email
    from src.security.cryptography.utils.salt import Salt
    from src.security.cryptography.blowfish_crypt import BlowfishCrypt
    
    password = HashedPassword(
        password="Password123",
        cryptography=BlowfishCrypt(),
        salt=Salt(b"salt_value")
    )
    
    mock_fiscal_repository.insert_all_from_fiscal.side_effect = Exception("Erro no repositório")
    use_case = InsertAllFiscalFromFiscalUseCase(mock_fiscal_repository)
    
    with pytest.raises(Exception):
        use_case.execute(
            name="Fiscal Teste",
            email=Email("fiscal@example.com"),
            password=password,
            phone="11999999999"
        )

def test_insert_all_fiscal_from_user_empty_name(mock_fiscal_repository):
    """Testa inserção de fiscal com nome vazio"""
    from src.domain.value_objects.email import Email
    from src.security.cryptography.utils.salt import Salt
    from src.security.cryptography.blowfish_crypt import BlowfishCrypt
    
    password = HashedPassword(
        password="Password123",
        cryptography=BlowfishCrypt(),
        salt=Salt(b"salt_value")
    )
    
    use_case = InsertAllFiscalFromFiscalUseCase(mock_fiscal_repository)
    
    use_case.execute(
        name="",
        email=Email("fiscal@example.com"),
        password=password,
        phone="11999999999"
    )
    
    mock_fiscal_repository.insert_all_from_fiscal.assert_called_once()
    call_args = mock_fiscal_repository.insert_all_from_fiscal.call_args
    assert call_args[0][0] == ""  # Primeiro argumento posicional
    assert call_args[0][1].email == "fiscal@example.com"  # Segundo argumento posicional
    assert call_args[0][3] == "11999999999"  # Quarto argumento posicional

# Testes para FindBairrobyId
def test_find_bairro_by_id_success(mock_bairro_repository, bairro_entity):
    """Testa busca de bairro por ID com sucesso"""
    mock_bairro_repository.find_by_id.return_value = bairro_entity
    use_case = FindBairrobyId(mock_bairro_repository)
    
    result = use_case.find(bairro_id=1)
    
    mock_bairro_repository.find_by_id.assert_called_once_with(bairro_id=1)
    assert isinstance(result, BairroEntity)
    assert result.bairro == 1
    assert result.name == "Bairro Teste"

def test_find_bairro_by_id_not_found(mock_bairro_repository):
    """Testa busca de bairro por ID quando não encontrado"""
    mock_bairro_repository.find_by_id.side_effect = AttributeError("Bairro não encontrado")
    use_case = FindBairrobyId(mock_bairro_repository)
    
    with pytest.raises(AttributeError):
        use_case.find(bairro_id=999)

def test_find_bairro_by_id_repository_error(mock_bairro_repository):
    """Testa busca de bairro por ID quando repositório lança exceção"""
    mock_bairro_repository.find_by_id.side_effect = Exception("Erro no repositório")
    use_case = FindBairrobyId(mock_bairro_repository)
    
    with pytest.raises(Exception):
        use_case.find(bairro_id=1)

# Testes para FindTypebyExactName
def test_find_type_by_exact_name_success(mock_types_repository, types_entity):
    """Testa busca de tipo por nome exato com sucesso"""
    mock_types_repository.find_by_name.return_value = types_entity
    use_case = FindTypebyExactName(mock_types_repository)
    
    result = use_case.find(name="Tipo Teste")
    
    mock_types_repository.find_by_name.assert_called_once_with(name="Tipo Teste")
    assert isinstance(result, TypesEntity)
    assert result.types_id == 1
    assert result.name == "Tipo Teste"

def test_find_type_by_exact_name_not_found(mock_types_repository):
    """Testa busca de tipo por nome exato quando não encontrado"""
    mock_types_repository.find_by_name.side_effect = AttributeError("Tipo não encontrado")
    use_case = FindTypebyExactName(mock_types_repository)
    
    with pytest.raises(AttributeError):
        use_case.find(name="Tipo Inexistente")

def test_find_type_by_exact_name_repository_error(mock_types_repository):
    """Testa busca de tipo por nome exato quando repositório lança exceção"""
    mock_types_repository.find_by_name.side_effect = Exception("Erro no repositório")
    use_case = FindTypebyExactName(mock_types_repository)
    
    with pytest.raises(Exception):
        use_case.find(name="Tipo Teste")

def test_find_type_by_exact_name_empty_name(mock_types_repository):
    """Testa busca de tipo por nome vazio"""
    mock_types_repository.find_by_name.side_effect = AttributeError("Tipo não encontrado")
    use_case = FindTypebyExactName(mock_types_repository)
    
    with pytest.raises(AttributeError):
        use_case.find(name="") 