import pytest
from src.data.use_cases.save_fiscal_document import SaveFiscalDocument
from src.domain.value_objects.generic_document import GenericDocument
from unittest.mock import Mock

class TestSaveFiscalDocument:
    
    def test_save_fiscal_document_success(self):
        # Arrange
        mock_repository = Mock()
        save_fiscal_document = SaveFiscalDocument(mock_repository)
        
        project_id = 123
        fiscal_id = 456
        documents = [
            GenericDocument(document=b"content1", document_name="relatorio.pdf", content_type="application/pdf"),
            GenericDocument(document=b"content2", document_name="foto.jpg", content_type="image/jpeg")
        ]
        
        # Act
        save_fiscal_document.save(project_id, fiscal_id, documents)
        
        # Assert
        mock_repository.insert_fiscal_documents.assert_called_once_with(
            project_id=project_id,
            fiscal_id=fiscal_id,
            documents=documents
        )
    
    def test_save_fiscal_document_repository_error(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.insert_fiscal_documents.side_effect = Exception("Database error")
        save_fiscal_document = SaveFiscalDocument(mock_repository)
        
        project_id = 123
        fiscal_id = 456
        documents = [GenericDocument(document=b"content", document_name="test.pdf", content_type="application/pdf")]
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            save_fiscal_document.save(project_id, fiscal_id, documents)
        
        assert 'Erro ao salvar documentos do fiscal 456 no projeto 123' in str(exc_info.value)
    
    def test_save_fiscal_document_empty_list(self):
        # Arrange
        mock_repository = Mock()
        save_fiscal_document = SaveFiscalDocument(mock_repository)
        
        project_id = 123
        fiscal_id = 456
        documents = []
        
        # Act
        save_fiscal_document.save(project_id, fiscal_id, documents)
        
        # Assert
        mock_repository.insert_fiscal_documents.assert_called_once_with(
            project_id=project_id,
            fiscal_id=fiscal_id,
            documents=documents
        ) 