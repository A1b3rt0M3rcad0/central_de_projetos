import pytest
from src.data.use_cases.delete_all_fiscal_documents_from_project import DeleteAllFiscalDocumentsFromProject
from unittest.mock import Mock

class TestDeleteAllFiscalDocumentsFromProject:
    
    def test_delete_all_fiscal_documents_success(self):
        # Arrange
        mock_repository = Mock()
        delete_all_fiscal_documents = DeleteAllFiscalDocumentsFromProject(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        
        # Act
        delete_all_fiscal_documents.delete_all(work_project_id, fiscal_id)
        
        # Assert
        mock_repository.delete_all_fiscal_documents_from_work_project.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id
        )
    
    def test_delete_all_fiscal_documents_repository_error(self):
        # Arrange
        mock_repository = Mock()
        mock_repository.delete_all_fiscal_documents_from_work_project.side_effect = Exception("Database error")
        delete_all_fiscal_documents = DeleteAllFiscalDocumentsFromProject(mock_repository)
        
        work_project_id = 123
        fiscal_id = 456
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            delete_all_fiscal_documents.delete_all(work_project_id, fiscal_id)
        
        assert 'Erro ao deletar todos os documentos do fiscal 456 no work project 123' in str(exc_info.value)
    
    def test_delete_all_fiscal_documents_different_ids(self):
        # Arrange
        mock_repository = Mock()
        delete_all_fiscal_documents = DeleteAllFiscalDocumentsFromProject(mock_repository)
        
        work_project_id = 999
        fiscal_id = 888
        
        # Act
        delete_all_fiscal_documents.delete_all(work_project_id, fiscal_id)
        
        # Assert
        mock_repository.delete_all_fiscal_documents_from_work_project.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id
        ) 