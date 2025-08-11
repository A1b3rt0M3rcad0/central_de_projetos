# pylint: disable=attribute-defined-outside-init,unused-import
import pytest
from unittest.mock import Mock
from src.data.use_cases.get_latest_work_project_image import GetLatestWorkProjectImage
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity

class TestGetLatestWorkProjectImage:
    
    def setup_method(self):  # pylint:disable=W0201
        """Setup method to initialize mocks before each test"""
        self.mock_project_document_repository = Mock(spec=IProjectDocumentFiscalRepository)
        self.mock_work_project_repository = Mock(spec=IWorkProjectRepository)
        self.use_case = GetLatestWorkProjectImage(
            self.mock_project_document_repository,
            self.mock_work_project_repository
        )
    
    def test_get_latest_image_success(self):
        """Test successful image retrieval"""
        # Arrange
        work_project_id = 1
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["image1.jpg", "document.pdf", "image2.png"]'
        
        self.mock_work_project_repository.find.return_value = mock_work_project
        self.mock_project_document_repository.get_document_by_work_project_and_name.return_value = b'image_data'
        
        # Act
        result = self.use_case.get_latest_image(work_project_id)
        
        # Assert
        assert result == b'image_data'
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_repository.get_document_by_work_project_and_name.assert_called_once_with(
            work_project_id=work_project_id,
            document_name="image2.png"
        )
    
    def test_get_latest_image_no_documents(self):
        """Test when work project has no documents"""
        # Arrange
        work_project_id = 1
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = None
        
        self.mock_work_project_repository.find.return_value = mock_work_project
        
        # Act
        result = self.use_case.get_latest_image(work_project_id)
        
        # Assert
        assert result is None
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_repository.get_document_by_work_project_and_name.assert_not_called()
    
    def test_get_latest_image_empty_documents_list(self):
        """Test when documents list is empty"""
        # Arrange
        work_project_id = 1
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '[]'
        
        self.mock_work_project_repository.find.return_value = mock_work_project
        
        # Act
        result = self.use_case.get_latest_image(work_project_id)
        
        # Assert
        assert result is None
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_repository.get_document_by_work_project_and_name.assert_not_called()
    
    def test_get_latest_image_no_images_in_documents(self):
        """Test when documents list has no images"""
        # Arrange
        work_project_id = 1
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["document.pdf", "report.docx"]'
        
        self.mock_work_project_repository.find.return_value = mock_work_project
        
        # Act
        result = self.use_case.get_latest_image(work_project_id)
        
        # Assert
        assert result is None
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_repository.get_document_by_work_project_and_name.assert_not_called()
    
    def test_get_latest_image_invalid_json(self):
        """Test when additional_documents is invalid JSON"""
        # Arrange
        work_project_id = 1
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = 'invalid json'
        
        self.mock_work_project_repository.find.return_value = mock_work_project
        
        # Act
        result = self.use_case.get_latest_image(work_project_id)
        
        # Assert
        assert result is None
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_repository.get_document_by_work_project_and_name.assert_not_called()
    
    def test_get_latest_image_document_not_found(self):
        """Test when document is not found in repository"""
        # Arrange
        work_project_id = 1
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.additional_documents = '["image1.jpg"]'
        
        self.mock_work_project_repository.find.return_value = mock_work_project
        self.mock_project_document_repository.get_document_by_work_project_and_name.side_effect = Exception("Document not found")
        
        # Act
        result = self.use_case.get_latest_image(work_project_id)
        
        # Assert
        assert result is None
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_repository.get_document_by_work_project_and_name.assert_called_once_with(
            work_project_id=work_project_id,
            document_name="image1.jpg"
        ) 