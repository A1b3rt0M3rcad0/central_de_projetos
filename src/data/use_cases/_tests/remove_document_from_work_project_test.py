#pylint:disable=all
import pytest
import json
from unittest.mock import Mock, patch
from src.data.use_cases.remove_document_from_work_project import RemoveDocumentFromWorkProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity

class TestRemoveDocumentFromWorkProject:
    
    def setup_method(self):
        """Setup method to initialize mocks before each test"""
        self.mock_repository = Mock(spec=IWorkProjectRepository)
        self.use_case = RemoveDocumentFromWorkProject(self.mock_repository)
    
    def test_remove_document_success_list_format(self):
        """Test successful document removal when documents are in list format"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.pdf"
        existing_documents = ["doc1.pdf", "test_document.pdf", "doc2.pdf"]
        expected_documents = ["doc1.pdf", "doc2.pdf"]
        
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = existing_documents
        
        self.mock_repository.find.return_value = mock_work_project
        
        # Act
        self.use_case.remove(work_project_id, document_name)
        
        # Assert
        self.mock_repository.find.assert_called_once_with(work_project_id)
        self.mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": expected_documents}
        )
    
    def test_remove_document_success_json_string_format(self):
        """Test successful document removal when documents are in JSON string format"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.pdf"
        existing_documents = ["doc1.pdf", "test_document.pdf", "doc2.pdf"]
        json_documents = json.dumps(existing_documents)
        expected_documents = ["doc1.pdf", "doc2.pdf"]
        
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = json_documents
        
        self.mock_repository.find.return_value = mock_work_project
        
        # Act
        self.use_case.remove(work_project_id, document_name)
        
        # Assert
        self.mock_repository.find.assert_called_once_with(work_project_id)
        self.mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": expected_documents}
        )
    
    def test_remove_document_not_found_in_list(self):
        """Test when document is not found in the list"""
        # Arrange
        work_project_id = 1
        document_name = "nonexistent_document.pdf"
        existing_documents = ["doc1.pdf", "doc2.pdf"]
        
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = existing_documents
        
        self.mock_repository.find.return_value = mock_work_project
        
        # Act
        self.use_case.remove(work_project_id, document_name)
        
        # Assert
        self.mock_repository.find.assert_called_once_with(work_project_id)
        self.mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": existing_documents}
        )
    
    def test_remove_document_none_documents(self):
        """Test when additional_documents is None"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.pdf"
        
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = None
        
        self.mock_repository.find.return_value = mock_work_project
        
        # Act
        self.use_case.remove(work_project_id, document_name)
        
        # Assert
        self.mock_repository.find.assert_called_once_with(work_project_id)
        self.mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": []}
        )
    
    def test_remove_document_invalid_json(self):
        """Test when additional_documents is invalid JSON"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.pdf"
        
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = "invalid json"
        
        self.mock_repository.find.return_value = mock_work_project
        
        # Act
        self.use_case.remove(work_project_id, document_name)
        
        # Assert
        self.mock_repository.find.assert_called_once_with(work_project_id)
        self.mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"additional_documents": []}
        )
    
    def test_remove_document_repository_error(self):
        """Test when repository raises an exception"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.pdf"
        expected_error = Exception("Repository error")
        
        self.mock_repository.find.side_effect = expected_error
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.use_case.remove(work_project_id, document_name)
        
        assert exc_info.value == expected_error
        self.mock_repository.find.assert_called_once_with(work_project_id) 