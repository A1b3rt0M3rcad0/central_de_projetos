# pylint:disable=W0611
import pytest
from unittest.mock import Mock
from src.presentation.controllers.update_project_andamento_controller import UpdateProjectAndamentoController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class TestUpdateProjectAndamentoController:
    
    def test_update_project_andamento_success(self):
        # Arrange
        mock_update_project_andamento = Mock()
        mock_create_history_project = Mock()
        
        controller = UpdateProjectAndamentoController(
            update_project_andamento_case=mock_update_project_andamento,
            create_history_project_case=mock_create_history_project
        )
        
        andamento = 'Concluído'
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'andamento_do_projeto': andamento
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'andamento_do_projeto updated'
        
        # Verifica se os use cases foram chamados corretamente
        mock_update_project_andamento.update.assert_called_once_with(
            project_id=123,
            andamento_do_projeto=andamento
        )
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='Andamento do Projeto',
            description=f'Andamento do projeto atualizado para {andamento}'
        )
    
    def test_update_project_andamento_error(self):
        # Arrange
        mock_update_project_andamento = Mock()
        mock_create_history_project = Mock()
        
        mock_update_project_andamento.update.side_effect = Exception("Erro ao atualizar andamento")
        
        controller = UpdateProjectAndamentoController(
            update_project_andamento_case=mock_update_project_andamento,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'andamento_do_projeto': 'Em andamento'
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao atualizar andamento' in str(exc_info.value)
        mock_create_history_project.create.assert_not_called()
    
    def test_update_project_andamento_history_error(self):
        # Arrange
        mock_update_project_andamento = Mock()
        mock_create_history_project = Mock()
        
        mock_create_history_project.create.side_effect = Exception("Erro ao criar histórico")
        
        controller = UpdateProjectAndamentoController(
            update_project_andamento_case=mock_update_project_andamento,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'andamento_do_projeto': 'Em andamento'
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao criar histórico' in str(exc_info.value)
        mock_update_project_andamento.update.assert_called_once()
    
    def test_update_project_andamento_empty_andamento(self):
        # Arrange
        mock_update_project_andamento = Mock()
        mock_create_history_project = Mock()
        
        controller = UpdateProjectAndamentoController(
            update_project_andamento_case=mock_update_project_andamento,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'andamento_do_projeto': ''
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'andamento_do_projeto updated'
        
        mock_update_project_andamento.update.assert_called_once_with(
            project_id=123,
            andamento_do_projeto=''
        )
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='Andamento do Projeto',
            description='Andamento do projeto atualizado para '
        ) 