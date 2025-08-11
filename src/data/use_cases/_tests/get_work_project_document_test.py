# pylint: disable=attribute-defined-outside-init,unused-import
import pytest
from unittest.mock import Mock
from src.data.use_cases.get_work_project_document import GetWorkProjectDocument
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository

class TestGetWorkProjectDocument:
    
    def setup_method(self):
        """Setup method to initialize mocks before each test"""
        self.mock_project_document_repository = Mock(spec=IProjectDocumentFiscalRepository)
        self.use_case = GetWorkProjectDocument(
            project_document_fiscal_repository=self.mock_project_document_repository
        )
    
    def test_get_document_success(self):
        """Test successful document retrieval"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.jpg"
        expected_data = b'document_binary_data'
        
        self.mock_project_document_repository.get_document_by_work_project_and_name.return_value = expected_data
        
        # Act
        result = self.use_case.get_document(work_project_id, document_name)
        
        # Assert
        assert result == expected_data
        self.mock_project_document_repository.get_document_by_work_project_and_name.assert_called_once_with(
            work_project_id=work_project_id,
            document_name=document_name
        )
    
    def test_get_document_repository_exception(self):
        """Test when repository raises an exception"""
        # Arrange
        work_project_id = 1
        document_name = "nonexistent_document.jpg"
        
        self.mock_project_document_repository.get_document_by_work_project_and_name.side_effect = Exception("Document not found")
        
        # Act & Assert
        with pytest.raises(Exception, match="Document not found"):
            self.use_case.get_document(work_project_id, document_name)
        
        self.mock_project_document_repository.get_document_by_work_project_and_name.assert_called_once_with(
            work_project_id=work_project_id,
            document_name=document_name
        )
    
    def test_get_document_with_different_types(self):
        """Test document retrieval with different file types"""
        # Arrange
        test_cases = [
            (1, "image.jpg", b'image_data'),
            (2, "document.pdf", b'pdf_data'),
            (3, "report.docx", b'docx_data'),
            (4, "data.xlsx", b'excel_data'),
        ]
        
        for work_project_id, document_name, expected_data in test_cases:
            self.mock_project_document_repository.get_document_by_work_project_and_name.return_value = expected_data
            
            # Act
            result = self.use_case.get_document(work_project_id, document_name)
            
            # Assert
            assert result == expected_data
            self.mock_project_document_repository.get_document_by_work_project_and_name.assert_called_with(
                work_project_id=work_project_id,
                document_name=document_name
            ) 