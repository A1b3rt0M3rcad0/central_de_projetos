# pylint:disable=W0611
import pytest
from unittest.mock import Mock
from src.presentation.controllers.find_all_history_from_project_controller import FindAllHistoryFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.history_project import HistoryProjectEntity
from datetime import datetime

class TestFindAllHistoryFromProjectController:
    
    def test_find_all_history_from_project_success(self):
        # Arrange
        mock_find_all_history_from_project = Mock()
        
        # Mock history entities
        mock_history1 = Mock(spec=HistoryProjectEntity)
        mock_history1.history_project_id = 1
        mock_history1.project_id = 123
        mock_history1.data_name = 'Nome'
        mock_history1.description = 'Nome do projeto atualizado para Teste'
        mock_history1.updated_at = datetime(2024, 1, 15, 10, 30, 0)
        
        mock_history2 = Mock(spec=HistoryProjectEntity)
        mock_history2.history_project_id = 2
        mock_history2.project_id = 123
        mock_history2.data_name = 'Data de inicio'
        mock_history2.description = 'Data de inicio do projeto atualizada para 2024-01-15'
        mock_history2.updated_at = datetime(2024, 1, 16, 14, 45, 0)
        
        mock_find_all_history_from_project.find.return_value = [mock_history1, mock_history2]
        
        controller = FindAllHistoryFromProjectController(
            find_all_history_from_project=mock_find_all_history_from_project
        )
        
        http_request = HttpRequest(
            path_params={'project_id': '123'}
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'History from project founded'
        assert len(response.body['content']) == 2
        
        # Verifica o primeiro histórico
        history1 = response.body['content'][0]
        assert history1['id'] == 1
        assert history1['project_id'] == 123
        assert history1['data_name'] == 'Nome'
        assert history1['description'] == 'Nome do projeto atualizado para Teste'
        assert history1['updated_at'] == '15/01/2024'
        
        # Verifica o segundo histórico
        history2 = response.body['content'][1]
        assert history2['id'] == 2
        assert history2['project_id'] == 123
        assert history2['data_name'] == 'Data de inicio'
        assert history2['description'] == 'Data de inicio do projeto atualizada para 2024-01-15'
        assert history2['updated_at'] == '16/01/2024'
        
        mock_find_all_history_from_project.find.assert_called_once_with(project_id='123')
    
    def test_find_all_history_from_project_empty_list(self):
        # Arrange
        mock_find_all_history_from_project = Mock()
        mock_find_all_history_from_project.find.return_value = []
        
        controller = FindAllHistoryFromProjectController(
            find_all_history_from_project=mock_find_all_history_from_project
        )
        
        http_request = HttpRequest(
            path_params={'project_id': '123'}
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'History from project founded'
        assert response.body['content'] == []
        
        mock_find_all_history_from_project.find.assert_called_once_with(project_id='123')
    
    def test_find_all_history_from_project_error(self):
        # Arrange
        mock_find_all_history_from_project = Mock()
        mock_find_all_history_from_project.find.side_effect = Exception("Erro ao buscar histórico")
        
        controller = FindAllHistoryFromProjectController(
            find_all_history_from_project=mock_find_all_history_from_project
        )
        
        http_request = HttpRequest(
            path_params={'project_id': '123'}
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao buscar histórico' in str(exc_info.value)
    
    def test_find_all_history_from_project_missing_project_id(self):
        # Arrange
        mock_find_all_history_from_project = Mock()
        
        controller = FindAllHistoryFromProjectController(
            find_all_history_from_project=mock_find_all_history_from_project
        )
        
        http_request = HttpRequest(
            path_params={}
        )
        
        # Act & Assert
        with pytest.raises(KeyError):
            controller.handle(http_request)
        
        mock_find_all_history_from_project.find.assert_not_called() 