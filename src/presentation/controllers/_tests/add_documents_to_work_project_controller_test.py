# pylint:disable=W0611
import pytest
from unittest.mock import Mock
from src.presentation.controllers.add_documents_to_work_project_controller import AddDocumentsToWorkProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.value_objects.document import Document

class TestAddDocumentsToWorkProjectController:
    
    def test_add_documents_to_work_project_success(self):
        # Arrange
        mock_save_fiscal_document = Mock()
        mock_update_work_project_documents = Mock()
        mock_get_work_project = Mock()
        mock_create_history_project = Mock()
        
        # Mock work_project existente
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = 456  # Adicionar project_id
        mock_get_work_project.get.return_value = mock_work_project
        
        controller = AddDocumentsToWorkProjectController(
            save_fiscal_document_case=mock_save_fiscal_document,
            update_work_project_documents_case=mock_update_work_project_documents,
            get_work_project_case=mock_get_work_project,
            create_history_project_case=mock_create_history_project
        )
        
        work_project_id = 123
        documents_data = [
            {
                'name': 'documento1.pdf',
                'content_type': 'application/pdf',
                'content': b'content1'
            },
            {
                'name': 'imagem.jpg',
                'content_type': 'image/jpeg',
                'content': b'content2'
            }
        ]
        
        http_request = HttpRequest(
            body={
                'work_project_id': work_project_id,
                'documents': documents_data
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert 'Documents added successfully' in response.body['message']
        assert response.body['documents_added'] == ['documento1.pdf', 'imagem.jpg']
        
        mock_get_work_project.get.assert_called_once_with(work_project_id=work_project_id)
        mock_save_fiscal_document.save.assert_called_once()
        mock_update_work_project_documents.update.assert_called_once()
    
    def test_add_documents_to_work_project_not_found(self):
        # Arrange
        mock_save_fiscal_document = Mock()
        mock_update_work_project_documents = Mock()
        mock_get_work_project = Mock()
        mock_create_history_project = Mock()
        
        # Mock work_project não encontrado
        mock_get_work_project.get.side_effect = Exception("Work project not found")
        
        controller = AddDocumentsToWorkProjectController(
            save_fiscal_document_case=mock_save_fiscal_document,
            update_work_project_documents_case=mock_update_work_project_documents,
            get_work_project_case=mock_get_work_project,
            create_history_project_case=mock_create_history_project
        )
        
        work_project_id = 999
        documents_data = [
            {
                'name': 'documento.pdf',
                'content_type': 'application/pdf',
                'content': b'content'
            }
        ]
        
        http_request = HttpRequest(
            body={
                'work_project_id': work_project_id,
                'documents': documents_data
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Work project not found' in str(exc_info.value)
        
        mock_get_work_project.get.assert_called_once_with(work_project_id=work_project_id)
        mock_save_fiscal_document.save.assert_not_called()
        mock_update_work_project_documents.update.assert_not_called()
    
    def test_add_documents_to_work_project_empty_documents(self):
        # Arrange
        mock_save_fiscal_document = Mock()
        mock_update_work_project_documents = Mock()
        mock_get_work_project = Mock()
        mock_create_history_project = Mock()
        
        # Mock work_project existente
        mock_work_project = Mock(spec=WorkProjectEntity)
        mock_work_project.project_id = 456  # Adicionar project_id
        mock_get_work_project.get.return_value = mock_work_project
        
        controller = AddDocumentsToWorkProjectController(
            save_fiscal_document_case=mock_save_fiscal_document,
            update_work_project_documents_case=mock_update_work_project_documents,
            get_work_project_case=mock_get_work_project,
            create_history_project_case=mock_create_history_project
        )
        
        work_project_id = 123
        documents_data = []
        
        http_request = HttpRequest(
            body={
                'work_project_id': work_project_id,
                'documents': documents_data
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['documents_added'] == []
        
        mock_get_work_project.get.assert_called_once_with(work_project_id=work_project_id)
        mock_save_fiscal_document.save.assert_called_once()
        mock_update_work_project_documents.update.assert_called_once() 