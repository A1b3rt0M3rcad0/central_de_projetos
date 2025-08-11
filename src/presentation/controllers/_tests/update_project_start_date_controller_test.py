# pylint:disable=W0611
import pytest
from unittest.mock import Mock
from src.presentation.controllers.update_project_start_date_controller import UpdateProjectStartDateController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from datetime import datetime

class TestUpdateProjectStartDateController:
    
    def test_update_project_start_date_success(self):
        # Arrange
        mock_update_project_start_date = Mock()
        mock_create_history_project = Mock()
        
        controller = UpdateProjectStartDateController(
            update_project_start_date_case=mock_update_project_start_date,
            create_history_project_case=mock_create_history_project
        )
        
        start_date = '2024-01-15'
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'start_date': start_date
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'Start date project updated'
        
        # Verifica se os use cases foram chamados corretamente
        expected_datetime = datetime.fromisoformat(start_date)
        mock_update_project_start_date.update.assert_called_once_with(
            project_id=123,
            start_date=expected_datetime
        )
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='Data de inicio',
            description=f'Data de inicio do projeto atualizada para {start_date}'
        )
    
    def test_update_project_start_date_error(self):
        # Arrange
        mock_update_project_start_date = Mock()
        mock_create_history_project = Mock()
        
        mock_update_project_start_date.update.side_effect = Exception("Erro ao atualizar data")
        
        controller = UpdateProjectStartDateController(
            update_project_start_date_case=mock_update_project_start_date,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'start_date': '2024-01-15'
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao atualizar data' in str(exc_info.value)
        mock_create_history_project.create.assert_not_called()
    
    def test_update_project_start_date_history_error(self):
        # Arrange
        mock_update_project_start_date = Mock()
        mock_create_history_project = Mock()
        
        mock_create_history_project.create.side_effect = Exception("Erro ao criar histórico")
        
        controller = UpdateProjectStartDateController(
            update_project_start_date_case=mock_update_project_start_date,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'start_date': '2024-01-15'
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao criar histórico' in str(exc_info.value)
        mock_update_project_start_date.update.assert_called_once()
    
    def test_update_project_start_date_invalid_date_format(self):
        # Arrange
        mock_update_project_start_date = Mock()
        mock_create_history_project = Mock()
        
        controller = UpdateProjectStartDateController(
            update_project_start_date_case=mock_update_project_start_date,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'start_date': 'data-invalida'
            }
        )
        
        # Act & Assert
        with pytest.raises(ValueError):
            controller.handle(http_request)
        
        mock_update_project_start_date.update.assert_not_called()
        mock_create_history_project.create.assert_not_called() 