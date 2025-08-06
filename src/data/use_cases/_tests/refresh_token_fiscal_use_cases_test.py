#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.create_refresh_token_fiscal import CreateRefreshTokenFiscal
from src.data.use_cases.update_refresh_token_fiscal import UpdateRefreshTokenFiscal
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

# Testes para CreateRefreshTokenFiscal
def test_create_refresh_token_fiscal_success(mock_fiscal_repository, fiscal_entity):
    """Testa criação de refresh token fiscal com sucesso"""
    from src.domain.value_objects.email import Email
    
    mock_fiscal_repository.find_by_email.return_value = fiscal_entity
    use_case = CreateRefreshTokenFiscal(mock_fiscal_repository)
    
    use_case.create(email=Email("fiscal@example.com"))
    
    mock_fiscal_repository.find_by_email.assert_called_once()
    call_args = mock_fiscal_repository.find_by_email.call_args
    assert call_args[0][0].email == "fiscal@example.com"  # Primeiro argumento posicional
    mock_fiscal_repository.insert_refresh_token.assert_called_once()
    call_args = mock_fiscal_repository.insert_refresh_token.call_args
    assert call_args[1]['fiscal_id'] == 1
    assert 'refresh_token' in call_args[1]

def test_create_refresh_token_fiscal_repository_error(mock_fiscal_repository):
    """Testa criação de refresh token fiscal quando repositório lança exceção"""
    from src.domain.value_objects.email import Email
    
    mock_fiscal_repository.find_by_email.side_effect = Exception("Erro no repositório")
    use_case = CreateRefreshTokenFiscal(mock_fiscal_repository)
    
    with pytest.raises(Exception):
        use_case.create(email=Email("fiscal@example.com"))

def test_create_refresh_token_fiscal_fiscal_not_found(mock_fiscal_repository):
    """Testa criação de refresh token fiscal quando fiscal não encontrado"""
    from src.domain.value_objects.email import Email
    
    mock_fiscal_repository.find_by_email.side_effect = AttributeError("Fiscal não encontrado")
    use_case = CreateRefreshTokenFiscal(mock_fiscal_repository)
    
    with pytest.raises(AttributeError):
        use_case.create(email=Email("fiscal@example.com"))

# Testes para UpdateRefreshTokenFiscal
def test_update_refresh_token_fiscal_success(mock_fiscal_repository, fiscal_entity):
    """Testa atualização de refresh token fiscal com sucesso"""
    from src.domain.value_objects.email import Email
    
    mock_fiscal_repository.find_by_email.return_value = fiscal_entity
    use_case = UpdateRefreshTokenFiscal(mock_fiscal_repository)
    
    new_token = "novo_token_123"
    use_case.update(fiscal_email=Email("fiscal@example.com"), new_token=new_token)
    
    mock_fiscal_repository.find_by_email.assert_called_once()
    call_args = mock_fiscal_repository.find_by_email.call_args
    assert call_args[0][0].email == "fiscal@example.com"  # Primeiro argumento posicional
    mock_fiscal_repository.insert_refresh_token.assert_called_once()
    call_args = mock_fiscal_repository.insert_refresh_token.call_args
    assert call_args[1]['fiscal_id'] == 1
    assert call_args[1]['refresh_token'] == new_token

def test_update_refresh_token_fiscal_repository_error(mock_fiscal_repository):
    """Testa atualização de refresh token fiscal quando repositório lança exceção"""
    from src.domain.value_objects.email import Email
    
    mock_fiscal_repository.find_by_email.side_effect = Exception("Erro no repositório")
    use_case = UpdateRefreshTokenFiscal(mock_fiscal_repository)
    
    with pytest.raises(Exception):
        use_case.update(fiscal_email=Email("fiscal@example.com"), new_token="novo_token")

def test_update_refresh_token_fiscal_fiscal_not_found(mock_fiscal_repository):
    """Testa atualização de refresh token fiscal quando fiscal não encontrado"""
    from src.domain.value_objects.email import Email
    
    mock_fiscal_repository.find_by_email.side_effect = AttributeError("Fiscal não encontrado")
    use_case = UpdateRefreshTokenFiscal(mock_fiscal_repository)
    
    with pytest.raises(AttributeError):
        use_case.update(fiscal_email=Email("fiscal@example.com"), new_token="novo_token")

def test_update_refresh_token_fiscal_empty_token(mock_fiscal_repository, fiscal_entity):
    """Testa atualização de refresh token fiscal com token vazio"""
    from src.domain.value_objects.email import Email
    
    mock_fiscal_repository.find_by_email.return_value = fiscal_entity
    use_case = UpdateRefreshTokenFiscal(mock_fiscal_repository)
    
    use_case.update(fiscal_email=Email("fiscal@example.com"), new_token="")
    
    mock_fiscal_repository.find_by_email.assert_called_once()
    call_args = mock_fiscal_repository.find_by_email.call_args
    assert call_args[0][0].email == "fiscal@example.com"  # Primeiro argumento posicional
    mock_fiscal_repository.insert_refresh_token.assert_called_once()
    call_args = mock_fiscal_repository.insert_refresh_token.call_args
    assert call_args[1]['fiscal_id'] == 1
    assert call_args[1]['refresh_token'] == "" 