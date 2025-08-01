import pytest
from src.presentation.controllers.login_fiscal_controller import LoginFiscalController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.errors.use_cases.fiscal_not_found_error import FiscalNotFoundError
from src.errors.use_cases.invalid_password_error import InvalidPasswordError
from unittest.mock import Mock

class TestLoginFiscalController:
    
    def test_login_fiscal_controller_success(self):
        # Arrange
        mock_login_fiscal_case = Mock()
        mock_login_fiscal_case.check.return_value = 'jwt_token'
        
        mock_create_refresh_token_fiscal = Mock()
        mock_update_refresh_token_fiscal = Mock()
        
        controller = LoginFiscalController(
            mock_login_fiscal_case,
            mock_create_refresh_token_fiscal,
            mock_update_refresh_token_fiscal
        )
        
        http_request = HttpRequest(
            body={
                'email': 'test@example.com',
                'password': 'Password123'
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert isinstance(response, HttpResponse)
        assert response.status_code == 200
        assert response.body['token'] == 'jwt_token'
        mock_login_fiscal_case.check.assert_called_once()
        
        # Verify the arguments passed to check method
        call_args = mock_login_fiscal_case.check.call_args
        assert isinstance(call_args.kwargs['email'], Email)
        assert call_args.kwargs['email'].email == 'test@example.com'
        assert isinstance(call_args.kwargs['password'], Password)
        assert call_args.kwargs['password'].password == 'Password123'
        
        # Verify refresh token was created
        mock_create_refresh_token_fiscal.create.assert_called_once()
        refresh_token_call_args = mock_create_refresh_token_fiscal.create.call_args
        assert isinstance(refresh_token_call_args.kwargs['email'], Email)
        assert refresh_token_call_args.kwargs['email'].email == 'test@example.com'
    
    def test_login_fiscal_controller_fiscal_not_found(self):
        # Arrange
        mock_login_fiscal_case = Mock()
        mock_login_fiscal_case.check.side_effect = FiscalNotFoundError(
            message='The fiscal with this email: test@example.com does not exists'
        )
        
        mock_create_refresh_token_fiscal = Mock()
        mock_update_refresh_token_fiscal = Mock()
        
        controller = LoginFiscalController(
            mock_login_fiscal_case,
            mock_create_refresh_token_fiscal,
            mock_update_refresh_token_fiscal
        )
        
        http_request = HttpRequest(
            body={
                'email': 'test@example.com',
                'password': 'Password123'
            }
        )
        
        # Act & Assert
        with pytest.raises(FiscalNotFoundError) as exc_info:
            controller.handle(http_request)
        
        assert 'The fiscal with this email: test@example.com does not exists' in str(exc_info.value.message)
    
    def test_login_fiscal_controller_invalid_password(self):
        # Arrange
        mock_login_fiscal_case = Mock()
        mock_login_fiscal_case.check.side_effect = InvalidPasswordError(
            message='The password Password123 is incorrect'
        )
        
        mock_create_refresh_token_fiscal = Mock()
        mock_update_refresh_token_fiscal = Mock()
        
        controller = LoginFiscalController(
            mock_login_fiscal_case,
            mock_create_refresh_token_fiscal,
            mock_update_refresh_token_fiscal
        )
        
        http_request = HttpRequest(
            body={
                'email': 'test@example.com',
                'password': 'Password123'
            }
        )
        
        # Act & Assert
        with pytest.raises(InvalidPasswordError) as exc_info:
            controller.handle(http_request)
        
        assert 'The password Password123 is incorrect' in str(exc_info.value.message) 