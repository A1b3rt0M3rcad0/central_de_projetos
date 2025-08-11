# pylint: disable=attribute-defined-outside-init,unused-import,unused-argument,unnecessary-pass
import pytest
from unittest.mock import Mock, patch
from src.main.composers.get_work_project_document_mobile_composer import get_work_project_document_mobile_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class TestGetWorkProjectDocumentMobileComposer:
    
    def setup_method(self):
        """Setup method to initialize test environment"""
        # pylint: disable=unnecessary-pass
        pass
    
    @patch('src.main.composers.get_work_project_document_mobile_composer.ProjectDocumentFiscalRepository')
    @patch('src.main.composers.get_work_project_document_mobile_composer.WorkProjectRepository')
    @patch('src.main.composers.get_work_project_document_mobile_composer.ProjectFiscalRepository')
    @patch('src.main.composers.get_work_project_document_mobile_composer.GetWorkProjectDocument')
    @patch('src.main.composers.get_work_project_document_mobile_composer.GetWorkProject')
    @patch('src.main.composers.get_work_project_document_mobile_composer.FindProjectFiscal')
    @patch('src.main.composers.get_work_project_document_mobile_composer.GetWorkProjectDocumentMobileController')
    @patch('src.main.composers.get_work_project_document_mobile_composer.raven_connection_handler_factory')
    @patch('src.main.composers.get_work_project_document_mobile_composer.db_connection_handler_factory')
    def test_composer_creates_handler_successfully(
        self,
        mock_db_factory,
        mock_raven_factory,
        mock_controller_class,
        mock_find_project_fiscal_class,
        mock_get_work_project_class,
        mock_get_work_project_document_class,
        mock_project_fiscal_repo_class,
        mock_work_project_repo_class,
        mock_project_document_repo_class
    ):
        """Test that composer creates handler successfully"""
        # Arrange
        mock_db_handler = Mock()
        mock_raven_handler = Mock()
        mock_controller = Mock()
        mock_controller.handle = Mock()
        
        mock_db_factory.return_value = mock_db_handler
        mock_raven_factory.return_value = mock_raven_handler
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = get_work_project_document_mobile_composer()
        
        # Assert
        assert handler is not None
        assert callable(handler)
        
        # Verify factories were called
        mock_db_factory.assert_called()
        mock_raven_factory.assert_called()
        
        # Verify repositories were instantiated
        mock_project_document_repo_class.assert_called_once_with(db_connection_handler=mock_raven_handler)
        mock_work_project_repo_class.assert_called_once_with(db_connection_handler=mock_db_handler)
        mock_project_fiscal_repo_class.assert_called_once_with(db_connection_handler=mock_db_handler)
        
        # Verify use cases were instantiated
        mock_get_work_project_document_class.assert_called_once()
        mock_get_work_project_class.assert_called_once()
        mock_find_project_fiscal_class.assert_called_once()
        
        # Verify controller was instantiated
        mock_controller_class.assert_called_once()
    
    @patch('src.main.composers.get_work_project_document_mobile_composer.ProjectDocumentFiscalRepository')
    @patch('src.main.composers.get_work_project_document_mobile_composer.WorkProjectRepository')
    @patch('src.main.composers.get_work_project_document_mobile_composer.ProjectFiscalRepository')
    @patch('src.main.composers.get_work_project_document_mobile_composer.GetWorkProjectDocument')
    @patch('src.main.composers.get_work_project_document_mobile_composer.GetWorkProject')
    @patch('src.main.composers.get_work_project_document_mobile_composer.FindProjectFiscal')
    @patch('src.main.composers.get_work_project_document_mobile_composer.GetWorkProjectDocumentMobileController')
    @patch('src.main.composers.get_work_project_document_mobile_composer.raven_connection_handler_factory')
    @patch('src.main.composers.get_work_project_document_mobile_composer.db_connection_handler_factory')
    def test_handler_returns_http_response(
        self,
        mock_db_factory,
        mock_raven_factory,
        mock_controller_class,
        mock_find_project_fiscal_class,
        mock_get_work_project_class,
        mock_get_work_project_document_class,
        mock_project_fiscal_repo_class,
        mock_work_project_repo_class,
        mock_project_document_repo_class
    ):
        """Test that handler returns HTTP response"""
        # Arrange
        mock_db_handler = Mock()
        mock_raven_handler = Mock()
        mock_controller = Mock()
        mock_response = Mock(spec=HttpResponse)
        mock_controller.handle.return_value = mock_response
        
        mock_db_factory.return_value = mock_db_handler
        mock_raven_factory.return_value = mock_raven_handler
        mock_controller_class.return_value = mock_controller
        
        # Create test request
        request = HttpRequest(
            path_params={
                "work_project_id": "1",
                "document_name": "test.jpg"
            },
            body={
                "fiscal_id": "5"
            }
        )
        
        # Act
        handler = get_work_project_document_mobile_composer()
        result = handler(request)
        
        # Assert
        assert result == mock_response
        mock_controller.handle.assert_called_once_with(request)
    
    @patch('src.main.composers.get_work_project_document_mobile_composer.ProjectDocumentFiscalRepository')
    @patch('src.main.composers.get_work_project_document_mobile_composer.WorkProjectRepository')
    @patch('src.main.composers.get_work_project_document_mobile_composer.ProjectFiscalRepository')
    @patch('src.main.composers.get_work_project_document_mobile_composer.GetWorkProjectDocument')
    @patch('src.main.composers.get_work_project_document_mobile_composer.GetWorkProject')
    @patch('src.main.composers.get_work_project_document_mobile_composer.FindProjectFiscal')
    @patch('src.main.composers.get_work_project_document_mobile_composer.GetWorkProjectDocumentMobileController')
    @patch('src.main.composers.get_work_project_document_mobile_composer.raven_connection_handler_factory')
    @patch('src.main.composers.get_work_project_document_mobile_composer.db_connection_handler_factory')
    def test_composer_dependencies_injection(
        self,
        mock_db_factory,
        mock_raven_factory,
        mock_controller_class,
        mock_find_project_fiscal_class,
        mock_get_work_project_class,
        mock_get_work_project_document_class,
        mock_project_fiscal_repo_class,
        mock_work_project_repo_class,
        mock_project_document_repo_class
    ):
        """Test that dependencies are properly injected"""
        # Arrange
        mock_db_handler = Mock()
        mock_raven_handler = Mock()
        mock_controller = Mock()
        
        mock_db_factory.return_value = mock_db_handler
        mock_raven_factory.return_value = mock_raven_handler
        mock_controller_class.return_value = mock_controller
        
        # Act
        get_work_project_document_mobile_composer()
        
        # Assert - Verify controller was called with correct dependencies
        mock_controller_class.assert_called_once()
        call_args = mock_controller_class.call_args
        
        # Verify all required dependencies were passed
        assert 'get_work_project_document_case' in call_args[1]
        assert 'get_work_project_case' in call_args[1]
        assert 'find_project_fiscal_case' in call_args[1]
        
        # Verify use cases were instantiated with correct repositories
        mock_get_work_project_document_class.assert_called_once()
        mock_get_work_project_class.assert_called_once()
        mock_find_project_fiscal_class.assert_called_once() 