import pytest
from unittest.mock import Mock
from src.data.use_cases.update_work_project_documents import UpdateWorkProjectDocuments
from src.domain.entities.work_project import WorkProjectEntity

class TestUpdateWorkProjectDocuments:
    
    def test_update_work_project_documents_success(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["existing1.pdf", "existing2.docx"]'
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectDocuments(mock_repository)
        work_project_id = 1
        additional_documents = '["documento1.pdf", "documento2.docx"]'
        
        # Act
        use_case.update(work_project_id, additional_documents)
        
        # Assert
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": ["existing1.pdf", "existing2.docx", "documento1.pdf", "documento2.docx"]}
        )
    
    def test_update_work_project_documents_no_existing_documents(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = None
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectDocuments(mock_repository)
        work_project_id = 1
        additional_documents = '["documento1.pdf", "documento2.docx"]'
        
        # Act
        use_case.update(work_project_id, additional_documents)
        
        # Assert
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": ["documento1.pdf", "documento2.docx"]}
        )
    
    def test_update_work_project_documents_empty_string_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectDocuments(mock_repository)
        work_project_id = 1
        additional_documents = ""
        
        # Act & Assert
        with pytest.raises(ValueError, match="Additional documents cannot be empty"):
            use_case.update(work_project_id, additional_documents)
        
        mock_repository.find.assert_not_called()
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_documents_whitespace_only_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectDocuments(mock_repository)
        work_project_id = 1
        additional_documents = "   "
        
        # Act & Assert
        with pytest.raises(ValueError, match="Additional documents cannot be empty"):
            use_case.update(work_project_id, additional_documents)
        
        mock_repository.find.assert_not_called()
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_documents_invalid_json_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectDocuments(mock_repository)
        work_project_id = 1
        additional_documents = "invalid json string"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Additional documents must be a valid JSON string"):
            use_case.update(work_project_id, additional_documents)
        
        mock_repository.find.assert_not_called()
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_documents_removes_duplicates(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["existing1.pdf", "existing2.docx"]'
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectDocuments(mock_repository)
        work_project_id = 1
        additional_documents = '["existing1.pdf", "new1.pdf", "existing2.docx", "new2.docx"]'
        
        # Act
        use_case.update(work_project_id, additional_documents)
        
        # Assert
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": ["existing1.pdf", "existing2.docx", "new1.pdf", "new2.docx"]}
        )
    
    def test_update_work_project_documents_single_document(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["existing1.pdf"]'
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectDocuments(mock_repository)
        work_project_id = 1
        additional_documents = '"new_document.pdf"'
        
        # Act
        use_case.update(work_project_id, additional_documents)
        
        # Assert
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": ["existing1.pdf", "new_document.pdf"]}
        )
    
    def test_update_work_project_documents_invalid_existing_json(self):
        # Arrange
        mock_repository = Mock()
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = 'invalid json'
        mock_repository.find.return_value = mock_work_project
        
        use_case = UpdateWorkProjectDocuments(mock_repository)
        work_project_id = 1
        additional_documents = '["new1.pdf", "new2.docx"]'
        
        # Act
        use_case.update(work_project_id, additional_documents)
        
        # Assert
        mock_repository.find.assert_called_once_with(work_project_id)
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": ["new1.pdf", "new2.docx"]}
        ) 