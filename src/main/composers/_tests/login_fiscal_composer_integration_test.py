import pytest
import time
from datetime import datetime
from src.presentation.controllers.login_fiscal_controller import LoginFiscalController
from src.data.use_cases.login_fiscal import LoginFiscal
from src.data.use_cases.create_refresh_token_fiscal import CreateRefreshTokenFiscal
from src.data.use_cases.update_refresh_token_fiscal import UpdateRefreshTokenFiscal
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.security.hashedpassword_factory import hashedpassword_factory
from src.errors.use_cases.fiscal_not_found_error import FiscalNotFoundError
from src.errors.use_cases.invalid_password_error import InvalidPasswordError
from src.infra.relational.config.connection.t_string_connection import TStringConnection
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.repository.fiscal_repository import FiscalRepository

# Import models to ensure SQLAlchemy can resolve relationships
# These imports are necessary for SQLAlchemy to properly configure relationships
# pylint: disable=unused-import
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.models.project import Project
from src.infra.relational.models.history_project import HistoryProject
from src.infra.relational.models.project_bairro import ProjectBairro
from src.infra.relational.models.project_empresa import ProjectEmpresa
from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.models.user_project import UserProject
from src.infra.relational.models.bairro import Bairro
from src.infra.relational.models.empresa import Empresa
from src.infra.relational.models.types import Types
from src.infra.relational.models.user import User
from src.infra.relational.models.status import Status
from src.infra.relational.models.refresh_token import RefreshToken
# pylint: enable=unused-import

class TestLoginFiscalComposerIntegration:
    
    def test_login_fiscal_composer_with_valid_credentials(self):
        # Arrange
        composer = LoginFiscalController(
            login_fiscal_case=LoginFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            ),
            create_refresh_token_fiscal=CreateRefreshTokenFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            ),
            update_refresh_token_fiscal=UpdateRefreshTokenFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            )
        ).handle
        
        # Create a test fiscal in the database
        
        fiscal_repository = FiscalRepository(DBConnectionHandler(TStringConnection()))
        
        # Create hashed password for test
        password = Password('TestPassword123')
        hashed_password = hashedpassword_factory(password)
        
        # Create unique email with timestamp
        timestamp = int(datetime.now().timestamp())
        unique_email = f'test.fiscal.valid.{timestamp}@example.com'
        
        # Insert test fiscal
        fiscal_repository.insert_all_from_fiscal(
            name='Test Fiscal',
            email=Email(unique_email),
            password=hashed_password,
            phone='1234567890'
        )
        
        http_request = HttpRequest(
            body={
                'email': unique_email,
                'password': 'TestPassword123'
            }
        )
        
        # Act
        response = composer(http_request)
        
        # Assert
        assert isinstance(response, HttpResponse)
        assert response.status_code == 200
        assert 'token' in response.body
        assert isinstance(response.body['token'], str)
        assert len(response.body['token']) > 0
        
        # Verify refresh token was stored in database
        fiscal = fiscal_repository.find_by_email(Email(unique_email))
        assert fiscal.refresh_token is not None
        assert len(fiscal.refresh_token) > 0
    
    def test_login_fiscal_composer_with_invalid_email(self):
        # Arrange
        composer = LoginFiscalController(
            login_fiscal_case=LoginFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            ),
            create_refresh_token_fiscal=CreateRefreshTokenFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            ),
            update_refresh_token_fiscal=UpdateRefreshTokenFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            )
        ).handle
        
        http_request = HttpRequest(
            body={
                'email': 'nonexistent@example.com',
                'password': 'TestPassword123'
            }
        )
        
        # Act & Assert
        with pytest.raises(FiscalNotFoundError) as exc_info:
            composer(http_request)
        
        assert 'does not exists' in str(exc_info.value.message)
    
    def test_login_fiscal_composer_with_invalid_password(self):
        # Arrange
        composer = LoginFiscalController(
            login_fiscal_case=LoginFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            ),
            create_refresh_token_fiscal=CreateRefreshTokenFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            ),
            update_refresh_token_fiscal=UpdateRefreshTokenFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            )
        ).handle
        
        # Create a test fiscal in the database
        fiscal_repository = FiscalRepository(DBConnectionHandler(TStringConnection()))
        
        # Create hashed password for test
        password = Password('TestPassword123')
        hashed_password = hashedpassword_factory(password)
        
        # Create unique email with timestamp
        timestamp = int(datetime.now().timestamp())
        unique_email = f'test.fiscal2.invalid.{timestamp}@example.com'
        
        # Insert test fiscal
        fiscal_repository.insert_all_from_fiscal(
            name='Test Fiscal 2',
            email=Email(unique_email),
            password=hashed_password,
            phone='1234567890'
        )
        
        http_request = HttpRequest(
            body={
                'email': unique_email,
                'password': 'WrongPassword123'
            }
        )
        
        # Act & Assert
        with pytest.raises(InvalidPasswordError) as exc_info:
            composer(http_request)
        
        assert 'incorrect' in str(exc_info.value.message)
    
    def test_login_fiscal_composer_refresh_token_update(self):
        # Arrange
        composer = LoginFiscalController(
            login_fiscal_case=LoginFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            ),
            create_refresh_token_fiscal=CreateRefreshTokenFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            ),
            update_refresh_token_fiscal=UpdateRefreshTokenFiscal(
                fiscal_repository=FiscalRepository(
                    db_connection_handler=DBConnectionHandler(TStringConnection())
                )
            )
        ).handle
        
        # Create a test fiscal in the database
        fiscal_repository = FiscalRepository(DBConnectionHandler(TStringConnection()))
        
        # Create hashed password for test
        password = Password('TestPassword123')
        hashed_password = hashedpassword_factory(password)
        
        # Create unique email with timestamp
        timestamp = int(datetime.now().timestamp())
        unique_email = f'test.fiscal3.refresh.{timestamp}@example.com'
        
        # Insert test fiscal
        fiscal_repository.insert_all_from_fiscal(
            name='Test Fiscal 3',
            email=Email(unique_email),
            password=hashed_password,
            phone='1234567890'
        )
        
        # First login - should create refresh token
        http_request1 = HttpRequest(
            body={
                'email': unique_email,
                'password': 'TestPassword123'
            }
        )
        
        response1 = composer(http_request1)
        assert response1.status_code == 200
        
        # Get first refresh token
        fiscal1 = fiscal_repository.find_by_email(Email(unique_email))
        first_refresh_token = fiscal1.refresh_token
        
        # Add a small delay to ensure different timestamps
        time.sleep(1)
        
        # Second login - should update refresh token
        response2 = composer(http_request1)
        assert response2.status_code == 200
        
        # Get second refresh token
        fiscal2 = fiscal_repository.find_by_email(Email(unique_email))
        second_refresh_token = fiscal2.refresh_token
        
        # Verify refresh token was updated (should be different)
        assert first_refresh_token != second_refresh_token
        assert first_refresh_token is not None
        assert second_refresh_token is not None 