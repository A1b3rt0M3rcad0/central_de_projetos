# pylint:disable=W0611
import pytest
from unittest.mock import Mock
from src.presentation.controllers.update_fiscal_from_project_controller import UpdateFiscalFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class TestUpdateFiscalFromProjectController:
    
    def test_update_fiscal_from_project_success(self):
        # Arrange
        mock_update_fiscal_from_project = Mock()
        mock_create_history_project = Mock()
        
        controller = UpdateFiscalFromProjectController(
            update_fiscal_from_project_case=mock_update_fiscal_from_project,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'fiscal_id': 1,
                'new_fiscal_id': 2
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'Fiscal from project updated'
        
        # Verifica se os use cases foram chamados corretamente
        mock_update_fiscal_from_project.update.assert_called_once_with(
            project_id=123,
            fiscal_id=1,
            new_fiscal_id=2
        )
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='Fiscal',
            description='Fiscal do projeto atualizado de 1 para 2'
        )
    
    def test_update_fiscal_from_project_error(self):
        # Arrange
        mock_update_fiscal_from_project = Mock()
        mock_create_history_project = Mock()
        
        mock_update_fiscal_from_project.update.side_effect = Exception("Erro ao atualizar fiscal")
        
        controller = UpdateFiscalFromProjectController(
            update_fiscal_from_project_case=mock_update_fiscal_from_project,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'fiscal_id': 1,
                'new_fiscal_id': 2
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao atualizar fiscal' in str(exc_info.value)
        mock_create_history_project.create.assert_not_called()
    
    def test_update_fiscal_from_project_history_error(self):
        # Arrange
        mock_update_fiscal_from_project = Mock()
        mock_create_history_project = Mock()
        
        mock_create_history_project.create.side_effect = Exception("Erro ao criar histórico")
        
        controller = UpdateFiscalFromProjectController(
            update_fiscal_from_project_case=mock_update_fiscal_from_project,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'fiscal_id': 1,
                'new_fiscal_id': 2
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao criar histórico' in str(exc_info.value)
        mock_update_fiscal_from_project.update.assert_called_once()
    
    def test_update_fiscal_from_project_same_fiscal(self):
        # Arrange
        mock_update_fiscal_from_project = Mock()
        mock_create_history_project = Mock()
        
        controller = UpdateFiscalFromProjectController(
            update_fiscal_from_project_case=mock_update_fiscal_from_project,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'project_id': 123,
                'fiscal_id': 1,
                'new_fiscal_id': 1
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'Fiscal from project updated'
        
        mock_update_fiscal_from_project.update.assert_called_once_with(
            project_id=123,
            fiscal_id=1,
            new_fiscal_id=1
        )
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='Fiscal',
            description='Fiscal do projeto atualizado de 1 para 1'
        ) 