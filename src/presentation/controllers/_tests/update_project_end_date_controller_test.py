# pylint:disable=W0611
import pytest
from unittest.mock import Mock
from src.presentation.controllers.update_project_end_date_controller import UpdateProjectEndDateController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from datetime import datetime

class TestUpdateProjectEndDateController:
    
    def test_update_project_end_date_success(self):
        # Arrange
        mock_update_project_end_date = Mock()
        mock_create_history_project = Mock()
        
        controller = UpdateProjectEndDateController(
            update_project_end_date_case=mock_update_project_end_date,
            create_history_project_case=mock_create_history_project
        )
        
        end_date = '2024-12-31'
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'end_date': end_date
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'end_date updated'
        
        # Verifica se os use cases foram chamados corretamente
        expected_datetime = datetime.fromisoformat(end_date)
        mock_update_project_end_date.update.assert_called_once_with(
            project_id=123,
            end_date=expected_datetime
        )
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='End Date',
            description=f'Data de finalização trocada para {end_date}'
        )
    
    def test_update_project_end_date_error(self):
        # Arrange
        mock_update_project_end_date = Mock()
        mock_create_history_project = Mock()
        
        mock_update_project_end_date.update.side_effect = Exception("Erro ao atualizar data de fim")
        
        controller = UpdateProjectEndDateController(
            update_project_end_date_case=mock_update_project_end_date,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'end_date': '2024-12-31'
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao atualizar data de fim' in str(exc_info.value)
        mock_create_history_project.create.assert_not_called()
    
    def test_update_project_end_date_history_error(self):
        # Arrange
        mock_update_project_end_date = Mock()
        mock_create_history_project = Mock()
        
        mock_create_history_project.create.side_effect = Exception("Erro ao criar histórico")
        
        controller = UpdateProjectEndDateController(
            update_project_end_date_case=mock_update_project_end_date,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'end_date': '2024-12-31'
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao criar histórico' in str(exc_info.value)
        mock_update_project_end_date.update.assert_called_once()
    
    def test_update_project_end_date_invalid_date_format(self):
        # Arrange
        mock_update_project_end_date = Mock()
        mock_create_history_project = Mock()
        
        controller = UpdateProjectEndDateController(
            update_project_end_date_case=mock_update_project_end_date,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'end_date': 'data-invalida'
            }
        )
        
        # Act & Assert
        with pytest.raises(ValueError):
            controller.handle(http_request)
        
        mock_update_project_end_date.update.assert_not_called()
        mock_create_history_project.create.assert_not_called() 