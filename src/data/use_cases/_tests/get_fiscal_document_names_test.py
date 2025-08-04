import pytest
from src.data.use_cases.get_fiscal_document_names import GetFiscalDocumentNames
from unittest.mock import Mock

class TestGetFiscalDocumentNames:
    
    def test_get_fiscal_document_names_success(self):
        # Arrange
        mock_repository = Mock()
        expected_names = ["relatorio.pdf", "foto.jpg", "laudo.docx"]
        mock_repository.get_fiscal_document_names.return_value = expected_names
        
        get_fiscal_document_names = GetFiscalDocumentNames(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        
        # Act
        result = get_fiscal_document_names.get_names(work_project_id, fiscal_id)
        
        # Assert
        assert result == expected_names
        mock_repository.get_fiscal_document_names.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id
        )
    
    def test_get_fiscal_document_names_empty_list(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.get_fiscal_document_names.return_value = []
        
        get_fiscal_document_names = GetFiscalDocumentNames(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        
        # Act
        result = get_fiscal_document_names.get_names(work_project_id, fiscal_id)
        
        # Assert
        assert result == []
        mock_repository.get_fiscal_document_names.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id
        )
    
    def test_get_fiscal_document_names_repository_exception(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.get_fiscal_document_names.side_effect = Exception("Database error")
        
        get_fiscal_document_names = GetFiscalDocumentNames(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            get_fiscal_document_names.get_names(work_project_id, fiscal_id)
        
        assert "Database error" in str(exc_info.value) 