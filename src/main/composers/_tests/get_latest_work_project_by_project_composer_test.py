#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.main.composers.get_latest_work_project_by_project_composer import get_latest_work_project_by_project_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime, timezone

class TestGetLatestWorkProjectByProjectComposer:
    
    def setup_method(self):
        self.mock_db_connection_handler = Mock()
        self.mock_work_project_repository = Mock()
        self.mock_use_case = Mock()
        self.mock_controller = Mock()
    
    @patch('src.main.composers.get_latest_work_project_by_project_composer.db_connection_handler_factory')
    @patch('src.main.composers.get_latest_work_project_by_project_composer.WorkProjectRepository')
    @patch('src.main.composers.get_latest_work_project_by_project_composer.GetLatestWorkProjectByProject')
    @patch('src.main.composers.get_latest_work_project_by_project_composer.GetLatestWorkProjectByProjectController')
    def test_composer_creates_handler_successfully(
        self, 
        mock_controller_class, 
        mock_use_case_class, 
        mock_repository_class, 
        mock_db_factory
    ):
        # Arrange
        mock_db_factory.return_value = self.mock_db_connection_handler
        mock_repository_class.return_value = self.mock_work_project_repository
        mock_use_case_class.return_value = self.mock_use_case
        mock_controller_class.return_value = self.mock_controller
        
        # Act
        handler = get_latest_work_project_by_project_composer()
        
        # Assert
        assert handler is not None
        assert callable(handler)
        
        # Verify dependencies were created correctly
        mock_db_factory.assert_called_once()
        mock_repository_class.assert_called_once_with(db_connection_handler=self.mock_db_connection_handler)
        mock_use_case_class.assert_called_once_with(work_project_repository=self.mock_work_project_repository)
        mock_controller_class.assert_called_once_with(
            get_latest_work_project_by_project_case=self.mock_use_case
        )
    
    @patch('src.main.composers.get_latest_work_project_by_project_composer.db_connection_handler_factory')
    @patch('src.main.composers.get_latest_work_project_by_project_composer.WorkProjectRepository')
    @patch('src.main.composers.get_latest_work_project_by_project_composer.GetLatestWorkProjectByProject')
    @patch('src.main.composers.get_latest_work_project_by_project_composer.GetLatestWorkProjectByProjectController')
    def test_composer_handler_returns_work_project_successfully(
        self, 
        mock_controller_class, 
        mock_use_case_class, 
        mock_repository_class, 
        mock_db_factory
    ):
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
        
        expected_response = HttpResponse(
            status_code=200,
            body={
                'message': 'Latest Work Project Found',
                'content': {
                    'id': 1,
                    'project_id': project_id,
                    'title': 'Trabalho Mais Recente',
                    'description': 'Descrição do trabalho mais recente',
                    'photo_name': 'foto_recente.jpg'
                }
            }
        )
        
        mock_db_factory.return_value = self.mock_db_connection_handler
        mock_repository_class.return_value = self.mock_work_project_repository
        mock_use_case_class.return_value = self.mock_use_case
        mock_controller_class.return_value = self.mock_controller
        self.mock_controller.handle.return_value = expected_response
        
        http_request = HttpRequest(
            path_params={'project_id': project_id},
            body={},
            headers={}
        )
        
        # Act
        handler = get_latest_work_project_by_project_composer()
        result = handler(http_request)
        
        # Assert
        assert result == expected_response
        self.mock_controller.handle.assert_called_once_with(http_request)
    
    @patch('src.main.composers.get_latest_work_project_by_project_composer.db_connection_handler_factory')
    @patch('src.main.composers.get_latest_work_project_by_project_composer.WorkProjectRepository')
    @patch('src.main.composers.get_latest_work_project_by_project_composer.GetLatestWorkProjectByProject')
    @patch('src.main.composers.get_latest_work_project_by_project_composer.GetLatestWorkProjectByProjectController')
    def test_composer_handler_returns_404_when_no_work_projects(
        self, 
        mock_controller_class, 
        mock_use_case_class, 
        mock_repository_class, 
        mock_db_factory
    ):
        # Arrange
        project_id = 1
        expected_response = HttpResponse(
            status_code=404,
            body={
                'message': 'No work projects found for this project',
                'content': None
            }
        )
        
        mock_db_factory.return_value = self.mock_db_connection_handler
        mock_repository_class.return_value = self.mock_work_project_repository
        mock_use_case_class.return_value = self.mock_use_case
        mock_controller_class.return_value = self.mock_controller
        self.mock_controller.handle.return_value = expected_response
        
        http_request = HttpRequest(
            path_params={'project_id': project_id},
            body={},
            headers={}
        )
        
        # Act
        handler = get_latest_work_project_by_project_composer()
        result = handler(http_request)
        
        # Assert
        assert result == expected_response
        assert result.status_code == 404
        assert result.body['message'] == 'No work projects found for this project'
        self.mock_controller.handle.assert_called_once_with(http_request) 