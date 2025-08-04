import pytest
from src.data.use_cases.delete_fiscal_document import DeleteFiscalDocument
from unittest.mock import Mock

class TestDeleteFiscalDocument:
    
    def test_delete_fiscal_document_success(self):
        # Arrange
        mock_repository = Mock()
        delete_fiscal_document = DeleteFiscalDocument(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        document_name = "relatorio.pdf"
        
        # Act
        delete_fiscal_document.delete(work_project_id, fiscal_id, document_name)
        
        # Assert
        mock_repository.delete_fiscal_document.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id,
            document_name=document_name
        )
    
    def test_delete_fiscal_document_repository_error(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.delete_fiscal_document.side_effect = Exception("Database error")
        delete_fiscal_document = DeleteFiscalDocument(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        document_name = "test.pdf"
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            delete_fiscal_document.delete(work_project_id, fiscal_id, document_name)
        
        assert 'Erro ao deletar documento "test.pdf" do fiscal 456 no work project 123' in str(exc_info.value)
    
    def test_delete_fiscal_document_with_special_characters(self):
        # Arrange
        mock_repository = Mock()
        delete_fiscal_document = DeleteFiscalDocument(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        document_name = "relatório com espaços.pdf"
        
        # Act
        delete_fiscal_document.delete(work_project_id, fiscal_id, document_name)
        
        # Assert
        mock_repository.delete_fiscal_document.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id,
            document_name=document_name
        ) 