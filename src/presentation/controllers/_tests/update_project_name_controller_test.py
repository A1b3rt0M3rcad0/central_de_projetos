# pylint:disable=W0611
import pytest
from unittest.mock import Mock
from src.presentation.controllers.update_project_name_controller import UpdateProjectNameController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class TestUpdateProjectNameController:
    
    def test_update_project_name_success(self):
        # Arrange
        mock_update_project_name = Mock()
        mock_create_history_project = Mock()
        
        controller = UpdateProjectNameController(
            update_project_name_case=mock_update_project_name,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'name': 'Novo Nome do Projeto'
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'project name updated'
        
        # Verifica se os use cases foram chamados corretamente
        mock_update_project_name.update.assert_called_once_with(
            project_id=123,
            name='Novo Nome do Projeto'
        )
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='Nome',
            description='Nome do projeto atualizado para Novo Nome do Projeto'
        )
    
    def test_update_project_name_error(self):
        # Arrange
        mock_update_project_name = Mock()
        mock_create_history_project = Mock()
        
        mock_update_project_name.update.side_effect = Exception("Erro ao atualizar nome")
        
        controller = UpdateProjectNameController(
            update_project_name_case=mock_update_project_name,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'name': 'Nome com Erro'
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao atualizar nome' in str(exc_info.value)
        mock_create_history_project.create.assert_not_called()
    
    def test_update_project_name_history_error(self):
        # Arrange
        mock_update_project_name = Mock()
        mock_create_history_project = Mock()
        
        mock_create_history_project.create.side_effect = Exception("Erro ao criar histórico")
        
        controller = UpdateProjectNameController(
            update_project_name_case=mock_update_project_name,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'name': 'Nome Teste'
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao criar histórico' in str(exc_info.value)
        mock_update_project_name.update.assert_called_once() 