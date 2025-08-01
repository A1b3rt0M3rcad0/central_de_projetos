import pytest
from src.data.use_cases.login_fiscal import LoginFiscal
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.errors.use_cases.fiscal_not_found_error import FiscalNotFoundError
from src.errors.use_cases.invalid_password_error import InvalidPasswordError
from unittest.mock import Mock

class TestLoginFiscal:
    
    def test_login_fiscal_success(self):
        # Arrange
        mock_repository = Mock()
        mock_fiscal_entity = Mock()
        mock_fiscal_entity.password = b'hashed_password'
        mock_fiscal_entity.salt = b'salt'
        mock_fiscal_entity.email = 'test@example.com'
        
        mock_repository.find_by_email.return_value = mock_fiscal_entity
        
        # Mock the hashedpassword_factory_chk to return True
        with pytest.MonkeyPatch().context() as m:
            m.setattr('src.data.use_cases.login_fiscal.hashedpassword_factory_chk', lambda pwd, salt, pwd_input: True)
            m.setattr('src.data.use_cases.login_fiscal.auth_factory', lambda: Mock(encode=lambda payload: 'jwt_token'))
            m.setattr('src.data.use_cases.login_fiscal.dotenv.load_dotenv', lambda: None)
            m.setattr('src.data.use_cases.login_fiscal.os.getenv', lambda key: '24')
            
            login_fiscal = LoginFiscal(mock_repository)
            email = Email('test@example.com')
            password = Password('Password123')
            
            # Act
            result = login_fiscal.check(email, password)
            
            # Assert
            assert result == 'jwt_token'
            mock_repository.find_by_email.assert_called_once_with(email=email)
    
    def test_login_fiscal_not_found(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.find_by_email.side_effect = AttributeError("Fiscal not found")
        
        login_fiscal = LoginFiscal(mock_repository)
        email = Email('nonexistent@example.com')
        password = Password('Password123')
        
        # Act & Assert
        with pytest.raises(FiscalNotFoundError) as exc_info:
            login_fiscal.check(email, password)
        
        assert 'The fiscal with this email: nonexistent@example.com does not exists' in str(exc_info.value.message)
    
    def test_login_fiscal_invalid_password(self):
        # Arrange
        mock_repository = Mock()
        mock_fiscal_entity = Mock()
        mock_fiscal_entity.password = b'hashed_password'
        mock_fiscal_entity.salt = b'salt'
        mock_fiscal_entity.email = 'test@example.com'
        
        mock_repository.find_by_email.return_value = mock_fiscal_entity
        
        # Mock the hashedpassword_factory_chk to return False
        with pytest.MonkeyPatch().context() as m:
            m.setattr('src.data.use_cases.login_fiscal.hashedpassword_factory_chk', lambda pwd, salt, pwd_input: False)
            
            login_fiscal = LoginFiscal(mock_repository)
            email = Email('test@example.com')
            password = Password('WrongPassword123')
            
            # Act & Assert
            with pytest.raises(InvalidPasswordError) as exc_info:
                login_fiscal.check(email, password)
            
            assert 'The password WrongPassword123 is incorrect' in str(exc_info.value.message) 