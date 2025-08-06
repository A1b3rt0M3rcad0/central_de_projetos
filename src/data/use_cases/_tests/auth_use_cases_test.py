#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.login import Login
from src.data.use_cases.create_refresh_token import CreateRefreshToken
from src.data.use_cases.update_refresh_token import UpdateRefreshToken
from src.data.use_cases.delete_refresh_token import DeleteRefreshToken
from src.data.use_cases.decode_jwt_token import DecodeJwtToken
from src.data.use_cases.encode_jwt import EncodeJwt
from src.data.use_cases.valid_jwt import ValidJwt
from src.domain.entities.user import UserEntity
from src.errors.use_cases.user_not_found_error import UserNotFoundError
from src.errors.use_cases.invalid_password_error import InvalidPasswordError

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def mock_jwt_handler():
    return MagicMock()

@pytest.fixture
def user_entity():
    from datetime import datetime
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.email import Email
    from src.domain.value_objects.roles import Role
    import bcrypt
    # Criar um salt válido do bcrypt
    salt = bcrypt.gensalt()
    password = "Password123"
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return UserEntity(
        cpf=CPF("12345678909"),
        password=hashed_password,
        salt=salt,
        role=Role("ADMIN"),
        email=Email("teste@example.com"),
        created_at=datetime.now(),
        name="Usuário Teste"
    )

def test_login_success(mock_repository, user_entity):
    """Testa login bem-sucedido"""
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.password import Password
    
    mock_repository.find.return_value = user_entity
    use_case = Login(mock_repository)
    
    result = use_case.check(CPF("12345678909"), Password("Password123"))
    
    # Verifica se o método foi chamado com o CPF correto
    mock_repository.find.assert_called_once()
    call_args = mock_repository.find.call_args
    assert call_args[1]['cpf'].value == "12345678909"
    assert isinstance(result, str)  # Retorna um token JWT

def test_login_user_not_found(mock_repository):
    """Testa login quando usuário não encontrado"""
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.password import Password
    mock_repository.find.side_effect = AttributeError("Usuário não encontrado")
    use_case = Login(mock_repository)
    
    with pytest.raises(UserNotFoundError):
        use_case.check(CPF("12345678909"), Password("Password123"))

def test_login_invalid_password(mock_repository, user_entity):
    """Testa login com senha inválida"""
    from src.domain.value_objects.cpf import CPF
    from src.domain.value_objects.password import Password
    mock_repository.find.return_value = user_entity
    use_case = Login(mock_repository)
    
    with pytest.raises(InvalidPasswordError):
        use_case.check(CPF("12345678909"), Password("WrongPass123"))

def test_create_refresh_token_success(mock_repository):
    """Testa criação de refresh token com sucesso"""
    from src.domain.value_objects.cpf import CPF
    use_case = CreateRefreshToken(mock_repository)
    
    use_case.create(CPF("12345678909"))
    
    # Verifica se foi chamado com os parâmetros corretos
    assert mock_repository.insert.called
    call_args = mock_repository.insert.call_args
    assert call_args[1]['user_cpf'].value == "12345678909"
    assert 'token' in call_args[1]

def test_create_refresh_token_repository_error(mock_repository):
    """Testa criação de refresh token quando repositório lança exceção"""
    from src.domain.value_objects.cpf import CPF
    mock_repository.insert.side_effect = Exception("Erro no repositório")
    use_case = CreateRefreshToken(mock_repository)
    
    with pytest.raises(Exception):
        use_case.create(CPF("12345678909"))

def test_update_refresh_token_success(mock_repository):
    """Testa atualização de refresh token com sucesso"""
    from src.domain.value_objects.cpf import CPF
    use_case = UpdateRefreshToken(mock_repository)
    
    use_case.update(CPF("12345678909"), "new_refresh_token_value")
    
    # Verifica se foi chamado com os parâmetros corretos
    assert mock_repository.update.called
    call_args = mock_repository.update.call_args
    assert call_args[1]['user_cpf'].value == "12345678909"
    assert call_args[1]['new_token'] == "new_refresh_token_value"

def test_update_refresh_token_repository_error(mock_repository):
    """Testa atualização de refresh token quando repositório lança exceção"""
    from src.domain.value_objects.cpf import CPF
    mock_repository.update.side_effect = Exception("Erro no repositório")
    use_case = UpdateRefreshToken(mock_repository)
    
    with pytest.raises(Exception):
        use_case.update(CPF("12345678909"), "new_refresh_token_value")

def test_delete_refresh_token_success(mock_repository):
    """Testa exclusão de refresh token com sucesso"""
    from src.domain.value_objects.cpf import CPF
    use_case = DeleteRefreshToken(mock_repository)
    
    use_case.delete(CPF("12345678909"))
    
    # Verifica se foi chamado com o parâmetro correto
    assert mock_repository.delete.called
    call_args = mock_repository.delete.call_args
    assert call_args[0][0].value == "12345678909"

def test_delete_refresh_token_repository_error(mock_repository):
    """Testa exclusão de refresh token quando repositório lança exceção"""
    from src.domain.value_objects.cpf import CPF
    mock_repository.delete.side_effect = Exception("Erro no repositório")
    use_case = DeleteRefreshToken(mock_repository)
    
    with pytest.raises(Exception):
        use_case.delete(CPF("12345678909"))

def test_decode_jwt_token_success(mock_jwt_handler):
    """Testa decodificação de JWT token com sucesso"""
    mock_jwt_handler.decode.return_value = {"user_id": 1, "email": "teste@example.com"}
    use_case = DecodeJwtToken(mock_jwt_handler)
    
    result = use_case.decode("jwt_token_value")
    
    mock_jwt_handler.decode.assert_called_once_with(token="jwt_token_value", verify_exp=True)
    assert result == {"user_id": 1, "email": "teste@example.com"}

def test_decode_jwt_token_invalid(mock_jwt_handler):
    """Testa decodificação de JWT token inválido"""
    mock_jwt_handler.decode.side_effect = Exception("Token inválido")
    use_case = DecodeJwtToken(mock_jwt_handler)
    
    with pytest.raises(Exception):
        use_case.decode("invalid_token")

def test_encode_jwt_success(mock_jwt_handler):
    """Testa codificação de JWT com sucesso"""
    mock_jwt_handler.encode.return_value = "encoded_jwt_token"
    use_case = EncodeJwt(mock_jwt_handler)
    
    result = use_case.encode({"user_id": 1, "email": "teste@example.com"})
    
    mock_jwt_handler.encode.assert_called_once_with(payload={"user_id": 1, "email": "teste@example.com"})
    assert result == "encoded_jwt_token"

def test_encode_jwt_error(mock_jwt_handler):
    """Testa codificação de JWT com erro"""
    mock_jwt_handler.encode.side_effect = Exception("Erro na codificação")
    use_case = EncodeJwt(mock_jwt_handler)
    
    with pytest.raises(Exception):
        use_case.encode({"user_id": 1, "email": "teste@example.com"})

def test_valid_jwt_success(mock_jwt_handler):
    """Testa validação de JWT válido"""
    mock_jwt_handler.is_expired.return_value = {"invalid": False, "expired": False}
    use_case = ValidJwt(mock_jwt_handler)
    
    result = use_case.valid("valid_jwt_token")
    
    mock_jwt_handler.is_expired.assert_called_once_with(token="valid_jwt_token")
    assert result == {"invalid": False, "expired": False}

def test_valid_jwt_invalid(mock_jwt_handler):
    """Testa validação de JWT inválido"""
    mock_jwt_handler.is_expired.return_value = {"invalid": True, "expired": False}
    use_case = ValidJwt(mock_jwt_handler)
    
    result = use_case.valid("invalid_jwt_token")
    
    mock_jwt_handler.is_expired.assert_called_once_with(token="invalid_jwt_token")
    assert result == {"invalid": True, "expired": False} 