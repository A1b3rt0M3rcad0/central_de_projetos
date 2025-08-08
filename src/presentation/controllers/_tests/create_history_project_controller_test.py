# pylint:disable=W0611
import pytest
from unittest.mock import Mock
from src.presentation.controllers.create_history_project_controller import CreateHistoryProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class TestCreateHistoryProjectController:
    
    def test_create_history_project_success(self):
        # Arrange
        mock_create_history_project = Mock()
        
        controller = CreateHistoryProjectController(
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'data_name': 'Nome',
                'description': 'Nome do projeto atualizado para Teste'
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'History Project created'
        
        # Verifica se o use case foi chamado corretamente
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='Nome',
            description='Nome do projeto atualizado para Teste'
        )
    
    def test_create_history_project_error(self):
        # Arrange
        mock_create_history_project = Mock()
        mock_create_history_project.create.side_effect = Exception("Erro ao criar histórico")
        
        controller = CreateHistoryProjectController(
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'data_name': 'Nome',
                'description': 'Nome do projeto atualizado para Teste'
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao criar histórico' in str(exc_info.value)
    
    def test_create_history_project_missing_project_id(self):
        # Arrange
        mock_create_history_project = Mock()
        
        controller = CreateHistoryProjectController(
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'data_name': 'Nome',
                'description': 'Nome do projeto atualizado para Teste'
            }
        )
        
        # Act & Assert
        with pytest.raises(KeyError):
            controller.handle(http_request)
        
        mock_create_history_project.create.assert_not_called()
    
    def test_create_history_project_missing_data_name(self):
        # Arrange
        mock_create_history_project = Mock()
        
        controller = CreateHistoryProjectController(
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'description': 'Nome do projeto atualizado para Teste'
            }
        )
        
        # Act & Assert
        with pytest.raises(KeyError):
            controller.handle(http_request)
        
        mock_create_history_project.create.assert_not_called()
    
    def test_create_history_project_missing_description(self):
        # Arrange
        mock_create_history_project = Mock()
        
        controller = CreateHistoryProjectController(
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'data_name': 'Nome'
            }
        )
        
        # Act & Assert
        with pytest.raises(KeyError):
            controller.handle(http_request)
        
        mock_create_history_project.create.assert_not_called()
    
    def test_create_history_project_empty_values(self):
        # Arrange
        mock_create_history_project = Mock()
        
        controller = CreateHistoryProjectController(
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'data_name': '',
                'description': ''
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'History Project created'
        
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='',
            description=''
        ) 