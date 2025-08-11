# pylint: disable=attribute-defined-outside-init,unused-import
import pytest
from unittest.mock import Mock
from src.presentation.controllers.get_work_project_document_mobile_controller import GetWorkProjectDocumentMobileController
from src.domain.use_cases.i_get_work_project_document import IGetWorkProjectDocument
from src.domain.use_cases.i_get_work_project import IGetWorkProject
from src.domain.use_cases.i_find_project_fiscal import IFindProjectFiscal
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.project_fiscal import ProjectFiscalEntity
from src.errors.use_cases.fiscal_not_authorized_error import FiscalNotAuthorizedError

class TestGetWorkProjectDocumentMobileController:
    
    def setup_method(self):
        """Setup method to initialize mocks before each test"""
        self.mock_get_work_project_document_case = Mock(spec=IGetWorkProjectDocument)
        self.mock_get_work_project_case = Mock(spec=IGetWorkProject)
        self.mock_find_project_fiscal_case = Mock(spec=IFindProjectFiscal)
        
        self.controller = GetWorkProjectDocumentMobileController(
            get_work_project_document_case=self.mock_get_work_project_document_case,
            get_work_project_case=self.mock_get_work_project_case,
            find_project_fiscal_case=self.mock_find_project_fiscal_case
        )
    
    def test_handle_success(self):
        """Test successful document retrieval"""
        # Arrange
        work_project_id = 1
        project_id = 10
        document_name = "test_document.jpg"
        fiscal_id = 5
        document_data = b'document_binary_data'
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = project_id
        
        # Mock project fiscal association
        mock_project_fiscal = Mock(spec=ProjectFiscalEntity)
        
        # Setup mocks
        self.mock_get_work_project_case.get.return_value = mock_work_project
        self.mock_find_project_fiscal_case.find.return_value = mock_project_fiscal
        self.mock_get_work_project_document_case.get_document.return_value = document_data
        
        # Create request
        request = HttpRequest(
            path_params={
                "work_project_id": str(work_project_id),
                "document_name": document_name
            },
            body={
                "fiscal_id": fiscal_id
            }
        )
        
        # Act
        result = self.controller.handle(request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body == document_data
        assert result.headers["Content-Type"] == "image/jpeg"
        assert result.headers["Content-Disposition"] == f'inline; filename="{document_name}"'
        
        # Verify use cases were called correctly
        self.mock_get_work_project_case.get.assert_called_once_with(work_project_id=work_project_id)
        self.mock_find_project_fiscal_case.find.assert_called_once_with(project_id=project_id, fiscal_id=fiscal_id)
        self.mock_get_work_project_document_case.get_document.assert_called_once_with(
            work_project_id=work_project_id,
            document_name=document_name
        )
    
    def test_handle_fiscal_not_authorized(self):
        """Test when fiscal is not authorized to access project documents"""
        # Arrange
        work_project_id = 1
        project_id = 10
        document_name = "test_document.jpg"
        fiscal_id = 5
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = project_id
        
        # Setup mocks - fiscal not found
        self.mock_get_work_project_case.get.return_value = mock_work_project
        self.mock_find_project_fiscal_case.find.side_effect = Exception("Fiscal not found")
        
        # Create request
        request = HttpRequest(
            path_params={
                "work_project_id": str(work_project_id),
                "document_name": document_name
            },
            body={
                "fiscal_id": fiscal_id
            }
        )
        
        # Act & Assert
        with pytest.raises(FiscalNotAuthorizedError):
            self.controller.handle(request)
        
        # Verify calls
        self.mock_get_work_project_case.get.assert_called_once_with(work_project_id=work_project_id)
        self.mock_find_project_fiscal_case.find.assert_called_once_with(project_id=project_id, fiscal_id=fiscal_id)
        self.mock_get_work_project_document_case.get_document.assert_not_called()
    
    def test_handle_different_content_types(self):
        """Test handling of different content types"""
        # Arrange
        test_cases = [
            ("document.pdf", "application/pdf"),
            ("image.jpg", "image/jpeg"),
        ]
        
        work_project_id = 1
        project_id = 10
        fiscal_id = 5
        document_data = b'document_data'
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = project_id
        
        # Mock project fiscal association
        mock_project_fiscal = Mock(spec=ProjectFiscalEntity)
        
        # Setup mocks
        self.mock_get_work_project_case.get.return_value = mock_work_project
        self.mock_find_project_fiscal_case.find.return_value = mock_project_fiscal
        self.mock_get_work_project_document_case.get_document.return_value = document_data
        
        for document_name, expected_content_type in test_cases:
            # Create request
            request = HttpRequest(
                path_params={
                    "work_project_id": str(work_project_id),
                    "document_name": document_name
                },
                body={
                    "fiscal_id": fiscal_id
                }
            )
            
            # Act
            result = self.controller.handle(request)
            
            # Assert
            assert result.status_code == 200
            assert result.body == document_data
            assert result.headers["Content-Type"] == expected_content_type
            assert result.headers["Content-Disposition"] == f'inline; filename="{document_name}"'
    
    def test_handle_missing_fiscal_id(self):
        """Test when fiscal_id is missing from request body"""
        # Arrange
        work_project_id = 1
        document_name = "test_document.jpg"
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = 10
        self.mock_get_work_project_case.get.return_value = mock_work_project
        
        # Mock find_project_fiscal to raise exception when fiscal_id is None
        self.mock_find_project_fiscal_case.find.side_effect = Exception("Fiscal not found")
        
        # Create request without fiscal_id
        request = HttpRequest(
            path_params={
                "work_project_id": str(work_project_id),
                "document_name": document_name
            },
            body={}
        )
        
        # Act & Assert
        with pytest.raises(FiscalNotAuthorizedError):
            self.controller.handle(request)
    
    def test_handle_document_not_found(self):
        """Test when document is not found"""
        # Arrange
        work_project_id = 1
        project_id = 10
        document_name = "nonexistent_document.jpg"
        fiscal_id = 5
        
        # Mock work project
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = project_id
        
        # Mock project fiscal association
        mock_project_fiscal = Mock(spec=ProjectFiscalEntity)
        
        # Setup mocks
        self.mock_get_work_project_case.get.return_value = mock_work_project
        self.mock_find_project_fiscal_case.find.return_value = mock_project_fiscal
        self.mock_get_work_project_document_case.get_document.side_effect = Exception("Document not found")
        
        # Create request
        request = HttpRequest(
            path_params={
                "work_project_id": str(work_project_id),
                "document_name": document_name
            },
            body={
                "fiscal_id": fiscal_id
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Document not found"):
            self.controller.handle(request)
        
        # Verify calls
        self.mock_get_work_project_case.get.assert_called_once_with(work_project_id=work_project_id)
        self.mock_find_project_fiscal_case.find.assert_called_once_with(project_id=project_id, fiscal_id=fiscal_id)
        self.mock_get_work_project_document_case.get_document.assert_called_once_with(
            work_project_id=work_project_id,
            document_name=document_name
        ) 