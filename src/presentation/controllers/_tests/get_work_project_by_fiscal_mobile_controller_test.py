#pylint:disable=all
import pytest
from unittest.mock import Mock
from src.presentation.controllers.get_work_project_by_fiscal_mobile_controller import GetWorkProjectByFiscalMobileController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime


class TestGetWorkProjectByFiscalMobileController:

    def test_controller_initialization(self):
        """Testa se o controller é inicializado corretamente"""
        # Arrange
        mock_use_case = Mock()
        
        # Act
        controller = GetWorkProjectByFiscalMobileController(
            get_work_project_by_fiscal_case=mock_use_case
        )
        
        # Assert
        assert controller is not None
        assert hasattr(controller, '_GetWorkProjectByFiscalMobileController__get_work_project_by_fiscal_case')

    def test_handle_with_valid_data(self):
        """Testa o método handle com dados válidos"""
        # Arrange
        mock_use_case = Mock()
        
        fiscal_entity = FiscalEntity(
            fiscal_id=1,
            name="Test Fiscal",
            created_at=datetime.now()
        )
        
        project_entity = ProjectEntity(
            project_id=1,
            status_id=1,
            verba_disponivel=MonetaryValue(100000.00),
            andamento_do_projeto="Em andamento",
            start_date=datetime.now(),
            expected_completion_date=datetime.now(),
            end_date=None,
            name="Test Project"
        )
        
        work_project_entity = WorkProjectEntity(
            id=1,
            project_id=1,
            fiscal_id=1,
            title="Test Work Project",
            description="Test Description",
            photo_name="test.jpg",
            additional_documents=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            fiscal=fiscal_entity,
            project=project_entity
        )
        
        mock_use_case.get.return_value = work_project_entity
        
        controller = GetWorkProjectByFiscalMobileController(
            get_work_project_by_fiscal_case=mock_use_case
        )
        
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'fiscal_id': 1
            }
        )
        
        # Act
        result = controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Work Project found successfully'
        assert result.body['content']['id'] == 1
        assert result.body['content']['title'] == 'Test Work Project'
        assert result.body['content']['fiscal']['name'] == 'Test Fiscal'
        assert result.body['content']['project']['name'] == 'Test Project'
        
        # Verifica se o use case foi chamado com os parâmetros corretos
        mock_use_case.get.assert_called_once_with(
            work_project_id=1,
            fiscal_id=1
        )

    def test_handle_with_missing_work_project_id(self):
        """Testa o método handle com work_project_id ausente"""
        # Arrange
        mock_use_case = Mock()
        controller = GetWorkProjectByFiscalMobileController(
            get_work_project_by_fiscal_case=mock_use_case
        )
        
        http_request = HttpRequest(
            body={
                'fiscal_id': 1
            }
        )
        
        # Act & Assert
        with pytest.raises(KeyError, match="work_project_id"):
            controller.handle(http_request)

    def test_handle_with_missing_fiscal_id(self):
        """Testa o método handle com fiscal_id ausente"""
        # Arrange
        mock_use_case = Mock()
        controller = GetWorkProjectByFiscalMobileController(
            get_work_project_by_fiscal_case=mock_use_case
        )
        
        http_request = HttpRequest(
            body={
                'work_project_id': 1
            }
        )
        
        # Act & Assert
        with pytest.raises(KeyError, match="fiscal_id"):
            controller.handle(http_request)

    def test_handle_with_use_case_exception(self):
        """Testa o método handle quando o use case lança exceção"""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.get.side_effect = Exception("Test error")
        
        controller = GetWorkProjectByFiscalMobileController(
            get_work_project_by_fiscal_case=mock_use_case
        )
        
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'fiscal_id': 1
            }
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Test error"):
            controller.handle(http_request)

    def test_handle_with_complete_work_project_data(self):
        """Testa o método handle com dados completos do work project"""
        # Arrange
        mock_use_case = Mock()
        
        fiscal_entity = FiscalEntity(
            fiscal_id=1,
            name="Complete Test Fiscal",
            created_at=datetime(2024, 1, 1, 10, 0, 0)
        )
        
        project_entity = ProjectEntity(
            project_id=1,
            status_id=1,
            verba_disponivel=MonetaryValue(500000.00),
            andamento_do_projeto="Concluído",
            start_date=datetime(2024, 1, 1),
            expected_completion_date=datetime(2024, 12, 31),
            end_date=datetime(2024, 11, 30),
            name="Complete Test Project"
        )
        
        work_project_entity = WorkProjectEntity(
            id=1,
            project_id=1,
            fiscal_id=1,
            title="Complete Test Work Project",
            description="Complete test description with more details",
            photo_name="complete_test.jpg",
            additional_documents=["doc1.pdf", "doc2.pdf"],
            created_at=datetime(2024, 1, 1, 10, 0, 0),
            updated_at=datetime(2024, 11, 30, 15, 30, 0),
            fiscal=fiscal_entity,
            project=project_entity
        )
        
        mock_use_case.get.return_value = work_project_entity
        
        controller = GetWorkProjectByFiscalMobileController(
            get_work_project_by_fiscal_case=mock_use_case
        )
        
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'fiscal_id': 1
            }
        )
        
        # Act
        result = controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Work Project found successfully'
        
        content = result.body['content']
        assert content['id'] == 1
        assert content['title'] == 'Complete Test Work Project'
        assert content['description'] == 'Complete test description with more details'
        assert content['photo_name'] == 'complete_test.jpg'
        assert content['additional_documents'] == ["doc1.pdf", "doc2.pdf"]
        assert content['fiscal']['name'] == 'Complete Test Fiscal'
        assert content['project']['name'] == 'Complete Test Project'
        assert content['project']['andamento_do_projeto'] == 'Concluído'
        assert content['project']['verba_disponivel'] == '$500000.00'

    def test_handle_with_none_fiscal_and_project(self):
        """Testa o método handle quando fiscal e project são None"""
        # Arrange
        mock_use_case = Mock()
        
        work_project_entity = WorkProjectEntity(
            id=1,
            project_id=1,
            fiscal_id=1,
            title="Test Work Project",
            description="Test Description",
            photo_name="test.jpg",
            additional_documents=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            fiscal=None,
            project=None
        )
        
        mock_use_case.get.return_value = work_project_entity
        
        controller = GetWorkProjectByFiscalMobileController(
            get_work_project_by_fiscal_case=mock_use_case
        )
        
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'fiscal_id': 1
            }
        )
        
        # Act
        result = controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Work Project found successfully'
        assert result.body['content']['id'] == 1
        assert result.body['content']['fiscal'] is None
        assert result.body['content']['project'] is None

    def test_handle_with_empty_additional_documents(self):
        """Testa o método handle com additional_documents vazio"""
        # Arrange
        mock_use_case = Mock()
        
        work_project_entity = WorkProjectEntity(
            id=1,
            project_id=1,
            fiscal_id=1,
            title="Test Work Project",
            description="Test Description",
            photo_name="test.jpg",
            additional_documents=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            fiscal=None,
            project=None
        )
        
        mock_use_case.get.return_value = work_project_entity
        
        controller = GetWorkProjectByFiscalMobileController(
            get_work_project_by_fiscal_case=mock_use_case
        )
        
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'fiscal_id': 1
            }
        )
        
        # Act
        result = controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['content']['additional_documents'] is None 