#pylint:disable=all
import pytest
from unittest.mock import Mock
from src.presentation.controllers.get_latest_work_project_by_project_controller import GetLatestWorkProjectByProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime, timezone

class TestGetLatestWorkProjectByProjectController:
    
    def setup_method(self):
        self.mock_use_case = Mock()
        self.controller = GetLatestWorkProjectByProjectController(self.mock_use_case)
    
    def test_handle_success(self):
        # Arrange
        project_id = 1
        fiscal_entity = FiscalEntity(
            fiscal_id=1,
            name="Fiscal Teste",
            created_at=datetime.now(timezone.utc)
        )
        project_entity = ProjectEntity(
            project_id=1,
            status_id=1,
            verba_disponivel=MonetaryValue(10000.0),
            andamento_do_projeto="Em andamento",
            start_date=datetime.now(timezone.utc),
            expected_completion_date=datetime.now(timezone.utc),
            end_date=None,
            name="Projeto Teste"
        )
        work_project_entity = WorkProjectEntity(
            id=1,
            project_id=project_id,
            fiscal_id=1,
            title="Trabalho Mais Recente",
            description="Descrição do trabalho mais recente",
            photo_name="foto_recente.jpg",
            additional_documents=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            fiscal=fiscal_entity,
            project=project_entity
        )
        
        self.mock_use_case.get_latest_by_project.return_value = work_project_entity
        
        http_request = HttpRequest(
            path_params={'project_id': project_id},
            body={},
            headers={}
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Latest Work Project Found'
        assert result.body['content'] is not None
        assert result.body['content']['id'] == 1
        assert result.body['content']['project_id'] == project_id
        assert result.body['content']['title'] == "Trabalho Mais Recente"
        assert result.body['content']['description'] == "Descrição do trabalho mais recente"
        assert result.body['content']['photo_name'] == "foto_recente.jpg"
        assert result.body['content']['fiscal'] is not None
        assert result.body['content']['fiscal']['name'] == "Fiscal Teste"
        assert result.body['content']['project'] is not None
        assert result.body['content']['project']['name'] == "Projeto Teste"
        
        self.mock_use_case.get_latest_by_project.assert_called_once_with(project_id=project_id)
    
    def test_handle_no_work_projects(self):
        # Arrange
        project_id = 1
        self.mock_use_case.get_latest_by_project.return_value = None
        
        http_request = HttpRequest(
            path_params={'project_id': project_id},
            body={},
            headers={}
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 404
        assert result.body['message'] == 'No work projects found for this project'
        assert result.body['content'] is None
        
        self.mock_use_case.get_latest_by_project.assert_called_once_with(project_id=project_id)
    
    def test_handle_use_case_error(self):
        # Arrange
        project_id = 1
        self.mock_use_case.get_latest_by_project.side_effect = Exception("Database error")
        
        http_request = HttpRequest(
            path_params={'project_id': project_id},
            body={},
            headers={}
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            self.controller.handle(http_request)
        
        self.mock_use_case.get_latest_by_project.assert_called_once_with(project_id=project_id)
    
    def test_handle_missing_project_id(self):
        # Arrange
        http_request = HttpRequest(
            path_params={},
            body={},
            headers={}
        )
        
        # Act & Assert
        with pytest.raises(KeyError):
            self.controller.handle(http_request) 