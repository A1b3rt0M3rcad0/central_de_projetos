#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.presentation.controllers.delete_document_from_work_project_mobile_controller import DeleteDocumentFromWorkProjectMobileController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.errors.use_cases.unauthorized_access_error import UnauthorizedAccessError

class TestDeleteDocumentFromWorkProjectMobileController:
    
    def setup_method(self):
        """Setup method to initialize mocks before each test"""
        self.mock_delete_fiscal_document_case = Mock()
        self.mock_remove_document_case = Mock()
        self.mock_get_work_project_case = Mock()
        self.mock_verify_association_case = Mock()
        self.mock_create_history_case = Mock()
        
        self.controller = DeleteDocumentFromWorkProjectMobileController(
            delete_fiscal_document_case=self.mock_delete_fiscal_document_case,
            remove_document_from_work_project_case=self.mock_remove_document_case,
            get_work_project_case=self.mock_get_work_project_case,
            verify_fiscal_work_project_association_case=self.mock_verify_association_case,
            create_history_project_case=self.mock_create_history_case
        )
    
    def test_handle_success(self):
        """Test successful document deletion"""
        # Arrange
        work_project_id = 1
        fiscal_id = 2
        document_name = "test_document.pdf"
        
        http_request = HttpRequest(
            body={
                'work_project_id': work_project_id,
                'document_name': document_name,
                'fiscal_id': fiscal_id
            }
        )
        
        self.mock_verify_association_case.verify.return_value = True
        self.mock_get_work_project_case.get.return_value = None
        
        # Act
        response = self.controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == f'Document "{document_name}" deleted successfully from work project {work_project_id}'
        assert response.body['work_project_id'] == work_project_id
        assert response.body['fiscal_id'] == fiscal_id
        assert response.body['document_name'] == document_name
        
        self.mock_verify_association_case.verify.assert_called_once_with(
            fiscal_id=fiscal_id,
            work_project_id=work_project_id
        )
        self.mock_get_work_project_case.get.assert_called_once_with(work_project_id=work_project_id)
        self.mock_delete_fiscal_document_case.delete.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id,
            document_name=document_name
        )
        self.mock_remove_document_case.remove.assert_called_once_with(
            work_project_id=work_project_id,
            document_name=document_name
        )
        self.mock_create_history_case.create.assert_called_once_with(
            project_id=work_project_id,
            data_name='Documento Mobile Deletado',
            description=f'Documento "{document_name}" deletado via mobile'
        )
    
    def test_handle_missing_fiscal_id(self):
        """Test when fiscal_id is missing from request"""
        # Arrange
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'document_name': "test_document.pdf"
                # fiscal_id is missing
            }
        )
        
        # Act & Assert
        with pytest.raises(UnauthorizedAccessError) as exc_info:
            self.controller.handle(http_request)
        
        assert "Fiscal ID não encontrado na requisição" in str(exc_info.value)
    
    def test_handle_fiscal_not_authorized(self):
        """Test when fiscal is not authorized to delete documents"""
        # Arrange
        work_project_id = 1
        fiscal_id = 2
        document_name = "test_document.pdf"
        
        http_request = HttpRequest(
            body={
                'work_project_id': work_project_id,
                'document_name': document_name,
                'fiscal_id': fiscal_id
            }
        )
        
        self.mock_verify_association_case.verify.return_value = False
        
        # Act & Assert
        with pytest.raises(UnauthorizedAccessError) as exc_info:
            self.controller.handle(http_request)
        
        assert f"Fiscal não está autorizado a deletar documentos deste work project" in str(exc_info.value)
    
    def test_handle_work_project_not_found(self):
        """Test when work project is not found"""
        # Arrange
        work_project_id = 1
        fiscal_id = 2
        document_name = "test_document.pdf"
        expected_error = Exception("Work project not found")
        
        http_request = HttpRequest(
            body={
                'work_project_id': work_project_id,
                'document_name': document_name,
                'fiscal_id': fiscal_id
            }
        )
        
        self.mock_verify_association_case.verify.return_value = True
        self.mock_get_work_project_case.get.side_effect = expected_error
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.controller.handle(http_request)
        
        assert exc_info.value == expected_error
    
    def test_handle_delete_document_error(self):
        """Test when document deletion fails"""
        # Arrange
        work_project_id = 1
        fiscal_id = 2
        document_name = "test_document.pdf"
        expected_error = Exception("Document deletion failed")
        
        http_request = HttpRequest(
            body={
                'work_project_id': work_project_id,
                'document_name': document_name,
                'fiscal_id': fiscal_id
            }
        )
        
        self.mock_verify_association_case.verify.return_value = True
        self.mock_get_work_project_case.get.return_value = None
        self.mock_delete_fiscal_document_case.delete.side_effect = expected_error
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.controller.handle(http_request)
        
        assert exc_info.value == expected_error 