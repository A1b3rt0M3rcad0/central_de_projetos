#pylint:disable=E0611
import pytest
from src.data.use_cases.get_fiscal_document import GetFiscalDocument
from src.domain.value_objects.generic_document import GenericDocument
from src.errors.use_cases.fiscal_document_not_found_error import FiscalDocumentNotFoundError
from unittest.mock import Mock

class TestGetFiscalDocument:
    
    def test_get_fiscal_document_success(self):
        # Arrange
        mock_repository = Mock()
        mock_document = GenericDocument(
            document=b"content",
            document_name="relatorio.pdf",
            content_type="application/pdf"
        )
        mock_repository.get_fiscal_document.return_value = mock_document
        
        get_fiscal_document = GetFiscalDocument(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        document_name = "relatorio.pdf"
        
        # Act
        result = get_fiscal_document.get(work_project_id, fiscal_id, document_name)
        
        # Assert
        assert result == mock_document
        mock_repository.get_fiscal_document.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id,
            document_name=document_name
        )
    
    def test_get_fiscal_document_not_found(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.get_fiscal_document.return_value = None
        
        get_fiscal_document = GetFiscalDocument(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        document_name = "inexistente.pdf"
        
        # Act & Assert
        with pytest.raises(FiscalDocumentNotFoundError) as exc_info:
            get_fiscal_document.get(work_project_id, fiscal_id, document_name)
        
        assert 'Documento "inexistente.pdf" do fiscal 456 não encontrado no work project 123' in str(exc_info.value.message)
    
    def test_get_fiscal_document_attribute_error(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.get_fiscal_document.side_effect = AttributeError("Document not found")
        
        get_fiscal_document = GetFiscalDocument(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        document_name = "test.pdf"
        
        # Act & Assert
        with pytest.raises(FiscalDocumentNotFoundError) as exc_info:
            get_fiscal_document.get(work_project_id, fiscal_id, document_name)
        
        assert 'Documento "test.pdf" do fiscal 456 não encontrado no work project 123' in str(exc_info.value.message)
    
    def test_get_fiscal_document_repository_exception(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.get_fiscal_document.side_effect = Exception("Database error")
        
        get_fiscal_document = GetFiscalDocument(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        document_name = "test.pdf"
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            get_fiscal_document.get(work_project_id, fiscal_id, document_name)
        
        assert "Database error" in str(exc_info.value) 