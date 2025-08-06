#pylint:disable=W0201
import pytest
from unittest.mock import Mock
from src.presentation.controllers.create_work_project_with_fiscal_document_controller import CreateWorkProjectWithFiscalDocumentController
from src.presentation.http_types.http_request import HttpRequest


class TestCreateWorkProjectWithFiscalDocumentController:
    
    def setup_method(self):
        self.mock_insert_work_project = Mock()
        self.mock_save_fiscal_document = Mock()
        self.mock_create_history_project = Mock()
        self.controller = CreateWorkProjectWithFiscalDocumentController(
            insert_work_project_case=self.mock_insert_work_project,
            save_fiscal_document_case=self.mock_save_fiscal_document,
            create_history_project_case=self.mock_create_history_project
        )
    
    def test_handle_success_with_documents(self):
        # Arrange
        request_body = {
            'project_id': 1,
            'fiscal_id': 2,
            'title': 'Fiscalização Teste',
            'description': 'Descrição da fiscalização',
            'additional_documents': [
                {
                    'content': b'fake_image_bytes',
                    'content_type': 'image/jpeg',
                    'name': 'foto_fiscalizacao.jpg'
                },
                {
                    'content': b'fake_pdf_bytes',
                    'content_type': 'application/pdf',
                    'name': 'relatorio_fiscal.pdf'
                }
            ]
        }
        
        http_request = HttpRequest(body=request_body)
        
        # Act
        response = self.controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'Work project created with fiscal documents successfully'
        assert response.body['title'] == 'Fiscalização Teste'
        assert response.body['photo_name'] == 'foto_fiscalizacao.jpg'
        assert response.body['documents_count'] == 2
        
        # Verificar se o caso de uso foi chamado corretamente
        self.mock_insert_work_project.insert.assert_called_once_with(
            project_id=1,
            fiscal_id=2,
            title='Fiscalização Teste',
            description='Descrição da fiscalização',
            photo_name='foto_fiscalizacao.jpg',
            additional_documents='["foto_fiscalizacao.jpg", "relatorio_fiscal.pdf"]'
        )
    
    def test_handle_success_without_documents(self):
        # Arrange
        request_body = {
            'project_id': 1,
            'fiscal_id': 2,
            'title': 'Fiscalização Teste',
            'description': 'Descrição da fiscalização'
        }
        
        http_request = HttpRequest(body=request_body)
        
        # Act
        response = self.controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'Work project created with fiscal documents successfully'
        assert response.body['title'] == 'Fiscalização Teste'
        assert response.body['photo_name'] is None
        assert response.body['documents_count'] == 0
        
        # Verificar se o caso de uso foi chamado corretamente
        self.mock_insert_work_project.insert.assert_called_once_with(
            project_id=1,
            fiscal_id=2,
            title='Fiscalização Teste',
            description='Descrição da fiscalização',
            photo_name=None,
            additional_documents=None
        )
    
    def test_handle_with_non_image_documents(self):
        # Arrange
        request_body = {
            'project_id': 1,
            'fiscal_id': 2,
            'title': 'Fiscalização Teste',
            'description': 'Descrição da fiscalização',
            'additional_documents': [
                {
                    'content': b'fake_pdf_bytes',
                    'content_type': 'application/pdf',
                    'name': 'relatorio_fiscal.pdf'
                }
            ]
        }
        
        http_request = HttpRequest(body=request_body)
        
        # Act
        response = self.controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['photo_name'] == 'relatorio_fiscal.pdf'  # Usa o primeiro documento como foto
        
        # Verificar se o caso de uso foi chamado corretamente
        self.mock_insert_work_project.insert.assert_called_once_with(
            project_id=1,
            fiscal_id=2,
            title='Fiscalização Teste',
            description='Descrição da fiscalização',
            photo_name='relatorio_fiscal.pdf',
            additional_documents='["relatorio_fiscal.pdf"]'
        )
    
    def test_handle_missing_required_fields(self):
        # Arrange
        request_body = {
            'project_id': 1,
            'fiscal_id': 2
            # Faltando title e description
        }
        
        http_request = HttpRequest(body=request_body)
        
        # Act & Assert
        with pytest.raises(KeyError):
            self.controller.handle(http_request) 