#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.data.use_cases.delete_fiscal_document_from_work_project import DeleteFiscalDocumentFromWorkProject
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository

class TestDeleteFiscalDocumentFromWorkProject:
    
    def setup_method(self):
        """Setup method to initialize mocks before each test"""
        self.mock_repository = Mock(spec=IProjectDocumentFiscalRepository)
        self.use_case = DeleteFiscalDocumentFromWorkProject(self.mock_repository)
    
    def test_delete_success(self):
        """Test successful document deletion"""
        # Arrange
        work_project_id = 1
        fiscal_id = 2
        document_name = "test_document.pdf"
        
        # Act
        self.use_case.delete(work_project_id, fiscal_id, document_name)
        
        # Assert
        self.mock_repository.delete_fiscal_document.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id,
            document_name=document_name
        )
    
    def test_delete_repository_error(self):
        """Test when repository raises an exception"""
        # Arrange
        work_project_id = 1
        fiscal_id = 2
        document_name = "test_document.pdf"
        expected_error = Exception("Repository error")
        
        self.mock_repository.delete_fiscal_document.side_effect = expected_error
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.use_case.delete(work_project_id, fiscal_id, document_name)
        
        assert exc_info.value == expected_error
        self.mock_repository.delete_fiscal_document.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id,
            document_name=document_name
        ) 