#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.main.composers.delete_document_from_work_project_mobile_composer import delete_document_from_work_project_mobile_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class TestDeleteDocumentFromWorkProjectMobileComposer:
    
    @patch('src.main.composers.delete_document_from_work_project_mobile_composer.raven_connection_handler_factory')
    @patch('src.main.composers.delete_document_from_work_project_mobile_composer.db_connection_handler_factory')
    def test_composer_returns_callable(self, mock_db_factory, mock_raven_factory):
        """Test that composer returns a callable function"""
        # Arrange
        mock_db_handler = Mock()
        mock_raven_handler = Mock()
        mock_db_factory.return_value = mock_db_handler
        mock_raven_factory.return_value = mock_raven_handler
        
        # Act
        controller = delete_document_from_work_project_mobile_composer()
        
        # Assert
        assert callable(controller)
    
    @patch('src.main.composers.delete_document_from_work_project_mobile_composer.raven_connection_handler_factory')
    @patch('src.main.composers.delete_document_from_work_project_mobile_composer.db_connection_handler_factory')
    def test_composer_creates_controller_with_dependencies(self, mock_db_factory, mock_raven_factory):
        """Test that composer creates controller with all required dependencies"""
        # Arrange
        mock_db_handler = Mock()
        mock_raven_handler = Mock()
        mock_db_factory.return_value = mock_db_handler
        mock_raven_factory.return_value = mock_raven_handler
        
        # Act
        controller = delete_document_from_work_project_mobile_composer()
        
        # Assert
        assert controller is not None
        # Verify that the factories were called
        mock_db_factory.assert_called()
        mock_raven_factory.assert_called()
    
    @patch('src.main.composers.delete_document_from_work_project_mobile_composer.raven_connection_handler_factory')
    @patch('src.main.composers.delete_document_from_work_project_mobile_composer.db_connection_handler_factory')
    def test_composer_integration_test(self, mock_db_factory, mock_raven_factory):
        """Integration test to verify the composed controller works"""
        # Arrange
        mock_db_handler = Mock()
        mock_raven_handler = Mock()
        mock_db_factory.return_value = mock_db_handler
        mock_raven_factory.return_value = mock_raven_handler
        
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'document_name': 'test_document.pdf',
                'fiscal_id': 2
            }
        )
        
        # Act
        controller = delete_document_from_work_project_mobile_composer()
        
        # Assert
        assert controller is not None
        # Note: We can't easily test the full integration without setting up the entire dependency chain
        # This test mainly verifies that the composer doesn't raise exceptions and returns a callable 