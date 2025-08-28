# pylint: disable=attribute-defined-outside-init,unused-import
import pytest
from unittest.mock import Mock
from src.presentation.controllers.download_work_project_document_controller import DownloadWorkProjectDocumentController
from src.domain.use_cases.i_get_work_project_document import IGetWorkProjectDocument
from src.domain.use_cases.i_get_work_project import IGetWorkProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.work_project import WorkProjectEntity

class TestDownloadWorkProjectDocumentController:
    
    def setup_method(self):
        """Setup method to initialize mocks before each test"""
        self.mock_get_work_project_document_case = Mock(spec=IGetWorkProjectDocument)
        self.mock_get_work_project_case = Mock(spec=IGetWorkProject)
        
        self.controller = DownloadWorkProjectDocumentController(
            get_work_project_document_case=self.mock_get_work_project_document_case,
            get_work_project_case=self.mock_get_work_project_case
        )
    
    def test_handle_success(self):
        """Test successful document download"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.pdf"
        document_data = b'document_binary_data'
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = 10
        
        # Setup mocks
        self.mock_get_work_project_case.get.return_value = mock_work_project
        self.mock_get_work_project_document_case.get_document.return_value = document_data
        
        # Create request
        request = HttpRequest(
            path_params={
                "work_project_id": str(work_project_id),
                "document_name": document_name
            }
        )
        
        # Act
        result = self.controller.handle(request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body == document_data
        assert result.headers["Content-Type"] == "application/pdf"
        assert result.headers["Content-Disposition"] == f'attachment; filename="{document_name}"'
        
        # Verify use cases were called correctly
        self.mock_get_work_project_case.get.assert_called_once_with(work_project_id=work_project_id)
        self.mock_get_work_project_document_case.get_document.assert_called_once_with(
            work_project_id=work_project_id,
            document_name=document_name
        )
    
    def test_handle_different_content_types(self):
        """Test handling of different content types for download"""
        # Arrange
        test_cases = [
            ("document.pdf", "application/pdf"),
            ("image.jpg", "image/jpeg"),
            ("document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            ("spreadsheet.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            ("presentation.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
        ]
        
        work_project_id = 1
        document_data = b'document_data'
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = 10
        
        # Setup mocks
        self.mock_get_work_project_case.get.return_value = mock_work_project
        self.mock_get_work_project_document_case.get_document.return_value = document_data
        
        for document_name, expected_content_type in test_cases:
            # Create request
            request = HttpRequest(
                path_params={
                    "work_project_id": str(work_project_id),
                    "document_name": document_name
                }
            )
            
            # Act
            result = self.controller.handle(request)
            
            # Assert
            assert result.status_code == 200
            assert result.body == document_data
            assert result.headers["Content-Type"] == expected_content_type
            assert result.headers["Content-Disposition"] == f'attachment; filename="{document_name}"'
    
    def test_handle_work_project_not_found(self):
        """Test when work project is not found"""
        # Arrange
        work_project_id = 999
        document_name = "test_document.pdf"
        
        # Setup mocks - work project not found
        self.mock_get_work_project_case.get.side_effect = Exception("Work project not found")
        
        # Create request
        request = HttpRequest(
            path_params={
                "work_project_id": str(work_project_id),
                "document_name": document_name
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Work project not found"):
            self.controller.handle(request)
        
        # Verify calls
        self.mock_get_work_project_case.get.assert_called_once_with(work_project_id=work_project_id)
        self.mock_get_work_project_document_case.get_document.assert_not_called()
    
    def test_handle_document_not_found(self):
        """Test when document is not found"""
        # Arrange
        work_project_id = 1
        document_name = "nonexistent_document.pdf"
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = 10
        
        # Setup mocks
        self.mock_get_work_project_case.get.return_value = mock_work_project
        self.mock_get_work_project_document_case.get_document.side_effect = Exception("Document not found")
        
        # Create request
        request = HttpRequest(
            path_params={
                "work_project_id": str(work_project_id),
                "document_name": document_name
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Document not found"):
            self.controller.handle(request)
        
        # Verify calls
        self.mock_get_work_project_case.get.assert_called_once_with(work_project_id=work_project_id)
        self.mock_get_work_project_document_case.get_document.assert_called_once_with(
            work_project_id=work_project_id,
            document_name=document_name
        )
    
    def test_handle_missing_path_params(self):
        """Test when path parameters are missing"""
        # Arrange
        request = HttpRequest(path_params={})
        
        # Act & Assert
        with pytest.raises(KeyError):
            self.controller.handle(request)
        
        # Verify no calls were made
        self.mock_get_work_project_case.get.assert_not_called()
        self.mock_get_work_project_document_case.get_document.assert_not_called()
    
    def test_handle_invalid_work_project_id(self):
        """Test when work_project_id is not a valid integer"""
        # Arrange
        document_name = "test_document.pdf"
        
        # Create request with invalid work_project_id
        request = HttpRequest(
            path_params={
                "work_project_id": "invalid_id",
                "document_name": document_name
            }
        )
        
        # Act & Assert
        with pytest.raises(ValueError):
            self.controller.handle(request)
        
        # Verify no calls were made
        self.mock_get_work_project_case.get.assert_not_called()
        self.mock_get_work_project_document_case.get_document.assert_not_called()
    
    def test_handle_empty_document_name(self):
        """Test when document name is empty"""
        # Arrange
        work_project_id = 1
        document_name = ""
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = 10
        
        # Setup mocks
        self.mock_get_work_project_case.get.return_value = mock_work_project
        self.mock_get_work_project_document_case.get_document.return_value = b'document_data'
        
        # Create request
        request = HttpRequest(
            path_params={
                "work_project_id": str(work_project_id),
                "document_name": document_name
            }
        )
        
        # Act
        result = self.controller.handle(request)
        
        # Assert
        assert result.status_code == 200
        assert result.headers["Content-Type"] == "application/octet-stream"
        assert result.headers["Content-Disposition"] == f'attachment; filename="{document_name}"'
    
    def test_handle_large_document(self):
        """Test handling of large document data"""
        # Arrange
        work_project_id = 1
        document_name = "large_document.pdf"
        document_data = b'x' * 1024 * 1024  # 1MB of data
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = 10
        
        # Setup mocks
        self.mock_get_work_project_case.get.return_value = mock_work_project
        self.mock_get_work_project_document_case.get_document.return_value = document_data
        
        # Create request
        request = HttpRequest(
            path_params={
                "work_project_id": str(work_project_id),
                "document_name": document_name
            }
        )
        
        # Act
        result = self.controller.handle(request)
        
        # Assert
        assert result.status_code == 200
        assert result.body == document_data
        assert len(result.body) == 1024 * 1024
        assert result.headers["Content-Type"] == "application/pdf"
        assert result.headers["Content-Disposition"] == f'attachment; filename="{document_name}"' 