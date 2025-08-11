# pylint:disable=W0611
import pytest
from unittest.mock import Mock
from src.presentation.controllers.create_project_controller import CreateProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime

class TestCreateProjectController:
    
    def test_create_project_success(self):
        # Arrange
        mock_create_project = Mock()
        mock_find_project_by_name = Mock()
        mock_create_history_project = Mock()
        
        # Mock project entity
        mock_project = Mock(spec=ProjectEntity)
        mock_project.project_id = 123
        mock_find_project_by_name.find.return_value = mock_project
        
        controller = CreateProjectController(
            create_project_case=mock_create_project,
            find_project_by_name_case=mock_find_project_by_name,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'status_id': 1,
                'name': 'Projeto Teste',
                'verba_disponivel': 10000.00,
                'andamento_do_projeto': 'Em andamento',
                'start_date': '2024-01-01',
                'expected_completion_date': '2024-12-31',
                'end_date': None
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'Project Created'
        
        # Verifica se os use cases foram chamados corretamente
        mock_create_project.create.assert_called_once()
        mock_find_project_by_name.find.assert_called_once_with(name='Projeto Teste')
        mock_create_history_project.create.assert_called_once_with(
            project_id=123,
            data_name='Project',
            description='Projeto Inserido'
        )
    
    def test_create_project_without_dates(self):
        # Arrange
        mock_create_project = Mock()
        mock_find_project_by_name = Mock()
        mock_create_history_project = Mock()
        
        mock_project = Mock(spec=ProjectEntity)
        mock_project.project_id = 456
        mock_find_project_by_name.find.return_value = mock_project
        
        controller = CreateProjectController(
            create_project_case=mock_create_project,
            find_project_by_name_case=mock_find_project_by_name,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'status_id': 1,
                'name': 'Projeto Sem Datas',
                'verba_disponivel': 5000.00,
                'andamento_do_projeto': 'Não iniciado',
                'start_date': None,
                'expected_completion_date': None,
                'end_date': None
            }
        )
        
        # Act
        response = controller.handle(http_request)
        
        # Assert
        assert response.status_code == 200
        assert response.body['message'] == 'Project Created'
        
        mock_create_project.create.assert_called_once()
        mock_create_history_project.create.assert_called_once()
    
    def test_create_project_error(self):
        # Arrange
        mock_create_project = Mock()
        mock_find_project_by_name = Mock()
        mock_create_history_project = Mock()
        
        mock_create_project.create.side_effect = Exception("Erro ao criar projeto")
        
        controller = CreateProjectController(
            create_project_case=mock_create_project,
            find_project_by_name_case=mock_find_project_by_name,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'status_id': 1,
                'name': 'Projeto Erro',
                'verba_disponivel': 1000.00,
                'andamento_do_projeto': 'Em andamento',
                'start_date': '2024-01-01',
                'expected_completion_date': '2024-12-31',
                'end_date': None
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Erro ao criar projeto' in str(exc_info.value)
        mock_create_history_project.create.assert_not_called()
    
    def test_create_project_find_project_error(self):
        # Arrange
        mock_create_project = Mock()
        mock_find_project_by_name = Mock()
        mock_create_history_project = Mock()
        
        mock_find_project_by_name.find.side_effect = Exception("Projeto não encontrado")
        
        controller = CreateProjectController(
            create_project_case=mock_create_project,
            find_project_by_name_case=mock_find_project_by_name,
            create_history_project_case=mock_create_history_project
        )
        
        http_request = HttpRequest(
            body={
                'status_id': 1,
                'name': 'Projeto Não Encontrado',
                'verba_disponivel': 1000.00,
                'andamento_do_projeto': 'Em andamento',
                'start_date': '2024-01-01',
                'expected_completion_date': '2024-12-31',
                'end_date': None
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            controller.handle(http_request)
        
        assert 'Projeto não encontrado' in str(exc_info.value)
        mock_create_history_project.create.assert_not_called() 