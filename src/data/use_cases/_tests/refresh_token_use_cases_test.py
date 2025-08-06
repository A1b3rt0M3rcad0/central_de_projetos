import pytest
from unittest.mock import MagicMock, patch
from src.data.use_cases.create_refresh_token import CreateRefreshToken
from src.data.use_cases.delete_refresh_token import DeleteRefreshToken
from src.domain.value_objects.cpf import CPF

@pytest.fixture
def mock_refresh_token_repository():
    return MagicMock()

@pytest.fixture
def valid_cpf():
    return CPF("12345678909")

def test_create_refresh_token_success(mock_refresh_token_repository, valid_cpf):
    with patch('src.data.use_cases.create_refresh_token.auth_factory') as mock_auth_factory:
        mock_encrypt = MagicMock()
        mock_encrypt.encode.return_value = "mock_refresh_token"
        mock_auth_factory.return_value = mock_encrypt
        
        with patch('src.data.use_cases.create_refresh_token.os.getenv') as mock_getenv:
            mock_getenv.return_value = "30"
            
            use_case = CreateRefreshToken(mock_refresh_token_repository)
            use_case.create(valid_cpf)
            
            mock_refresh_token_repository.insert.assert_called_once()
            call_args = mock_refresh_token_repository.insert.call_args
            assert call_args[1]['user_cpf'] == valid_cpf
            assert call_args[1]['token'] == "mock_refresh_token"

def test_create_refresh_token_repository_error(mock_refresh_token_repository, valid_cpf):
    mock_refresh_token_repository.insert.side_effect = Exception("Repository error")
    
    with patch('src.data.use_cases.create_refresh_token.auth_factory') as mock_auth_factory:
        mock_encrypt = MagicMock()
        mock_encrypt.encode.return_value = "mock_refresh_token"
        mock_auth_factory.return_value = mock_encrypt
        
        with patch('src.data.use_cases.create_refresh_token.os.getenv') as mock_getenv:
            mock_getenv.return_value = "30"
            
            use_case = CreateRefreshToken(mock_refresh_token_repository)
            
            with pytest.raises(Exception, match="Repository error"):
                use_case.create(valid_cpf)

def test_create_refresh_token_invalid_expire_time(mock_refresh_token_repository, valid_cpf):
    with patch('src.data.use_cases.create_refresh_token.os.getenv') as mock_getenv:
        mock_getenv.return_value = "invalid"
        
        use_case = CreateRefreshToken(mock_refresh_token_repository)
        
        with pytest.raises(ValueError, match="The EXPIRE_TIME_REFRESH_TOKEN value is invalid"):
            use_case.create(valid_cpf)

def test_create_refresh_token_none_expire_time(mock_refresh_token_repository, valid_cpf):
    with patch('src.data.use_cases.create_refresh_token.os.getenv') as mock_getenv:
        mock_getenv.return_value = None
        
        use_case = CreateRefreshToken(mock_refresh_token_repository)
        
        with pytest.raises(ValueError, match="The EXPIRE_TIME_REFRESH_TOKEN value is invalid"):
            use_case.create(valid_cpf)

def test_delete_refresh_token_success(mock_refresh_token_repository, valid_cpf):
    use_case = DeleteRefreshToken(mock_refresh_token_repository)
    use_case.delete(valid_cpf)
    
    mock_refresh_token_repository.delete.assert_called_once_with(valid_cpf)

def test_delete_refresh_token_repository_error(mock_refresh_token_repository, valid_cpf):
    mock_refresh_token_repository.delete.side_effect = Exception("Repository error")
    
    use_case = DeleteRefreshToken(mock_refresh_token_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(valid_cpf) 