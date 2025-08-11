#pylint:disable=all
import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime, timezone
from src.presentation.controllers.get_work_projects_by_fiscal_mobile_controller import GetWorkProjectsByFiscalMobileController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from src.errors.use_cases.fiscal_not_authorized_error import FiscalNotAuthorizedError
from src.errors.repository.not_exists_error.projects_from_fiscal_does_not_exists import ProjectFiscalNotExists


class TestGetWorkProjectsByFiscalMobileController:

    def setup_method(self):
        """Setup para cada teste"""
        self.mock_get_work_projects_case = Mock()
        self.mock_find_project_fiscal_case = Mock()
        
        self.controller = GetWorkProjectsByFiscalMobileController(
            get_work_projects_by_fiscal_mobile_case=self.mock_get_work_projects_case,
            find_project_fiscal_case=self.mock_find_project_fiscal_case
        )

    def test_handle_success(self):
        """Testa o sucesso da operação com dados válidos"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        page = 1
        page_size = 10
        
        # Mock fiscal entity
        fiscal_entity = FiscalEntity(
            fiscal_id=fiscal_id,
            name="Fiscal Teste",
            created_at=datetime.now(timezone.utc)
        )
        
        # Mock project entity
        project_entity = ProjectEntity(
            project_id=project_id,
            status_id=1,
            name="Projeto Teste",
            andamento_do_projeto="Em andamento",
            verba_disponivel=MonetaryValue(1000.0),
            start_date=datetime.now(timezone.utc),
            expected_completion_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc)
        )
        
        # Mock work project entity
        work_project_entity = WorkProjectEntity(
            id=1,
            project_id=project_id,
            fiscal_id=fiscal_id,
            title="Work Project Teste",
            description="Descrição do work project",
            photo_name="foto.jpg",
            additional_documents=["doc1.pdf", "doc2.pdf"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            fiscal=fiscal_entity,
            project=project_entity
        )
        
        # Mock HTTP request
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            path_params={
                'project_id': project_id,
                'page': page,
                'page_size': page_size
            }
        )
        
        # Mock responses
        self.mock_find_project_fiscal_case.find.return_value = Mock()
        self.mock_get_work_projects_case.get_by_fiscal_mobile.return_value = {
            'total': 1,
            'data': [work_project_entity]
        }
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['message'] == 'Work Projects Founded'
        assert result.body['total'] == 1
        assert result.body['page'] == page
        assert result.body['page_size'] == page_size
        assert result.body['project_id'] == project_id
        assert result.body['fiscal_id'] == fiscal_id
        assert len(result.body['content']) == 1
        
        # Verificar se os métodos foram chamados corretamente
        self.mock_find_project_fiscal_case.find.assert_called_once_with(
            project_id=project_id,
            fiscal_id=fiscal_id
        )
        self.mock_get_work_projects_case.get_by_fiscal_mobile.assert_called_once_with(
            fiscal_id=fiscal_id,
            project_id=project_id,
            page=page,
            page_size=page_size
        )

    def test_handle_missing_fiscal_id(self):
        """Testa erro quando fiscal_id não é fornecido"""
        # Arrange
        http_request = HttpRequest(
            body={},
            path_params={
                'project_id': 1,
                'page': 1,
                'page_size': 10
            }
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert result.status_code == 400
        assert result.body['error'] == 'fiscal_id is required'

    def test_handle_missing_project_id(self):
        """Testa erro quando project_id não é fornecido"""
        # Arrange
        http_request = HttpRequest(
            body={'fiscal_id': 1},
            path_params={
                'page': 1,
                'page_size': 10
            }
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert result.status_code == 400
        assert result.body['error'] == 'project_id is required'

    def test_handle_fiscal_not_authorized(self):
        """Testa erro quando fiscal não está autorizado para o projeto"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            path_params={
                'project_id': project_id,
                'page': 1,
                'page_size': 10
            }
        )
        
        # Mock para simular fiscal não autorizado
        self.mock_find_project_fiscal_case.find.side_effect = ProjectFiscalNotExists(
            message=f'The project fiscal association ({fiscal_id}, {project_id}) does not exists'
        )
        
        # Act & Assert
        with pytest.raises(FiscalNotAuthorizedError) as exc_info:
            self.controller.handle(http_request)
        
        assert "Fiscal 1 não está autorizado a acessar work projects do projeto 2" in str(exc_info.value)

    def test_handle_empty_work_projects_list(self):
        """Testa quando não há work projects para o fiscal/projeto"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        page = 1
        page_size = 10
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            path_params={
                'project_id': project_id,
                'page': page,
                'page_size': page_size
            }
        )
        
        # Mock responses
        self.mock_find_project_fiscal_case.find.return_value = Mock()
        self.mock_get_work_projects_case.get_by_fiscal_mobile.return_value = {
            'total': 0,
            'data': []
        }
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['total'] == 0
        assert len(result.body['content']) == 0

    def test_handle_multiple_work_projects(self):
        """Testa com múltiplos work projects"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        page = 1
        page_size = 10
        
        # Mock entities
        fiscal_entity = FiscalEntity(
            fiscal_id=fiscal_id,
            name="Fiscal Teste",
            created_at=datetime.now(timezone.utc)
        )
        
        project_entity = ProjectEntity(
            project_id=project_id,
            status_id=1,
            name="Projeto Teste",
            andamento_do_projeto="Em andamento",
            verba_disponivel=MonetaryValue(1000.0),
            start_date=datetime.now(timezone.utc),
            expected_completion_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc)
        )
        
        # Criar múltiplos work projects
        work_projects = []
        for i in range(3):
            work_project = WorkProjectEntity(
                id=i+1,
                project_id=project_id,
                fiscal_id=fiscal_id,
                title=f"Work Project {i+1}",
                description=f"Descrição {i+1}",
                photo_name=f"foto{i+1}.jpg",
                additional_documents=[f"doc{i+1}.pdf"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                fiscal=fiscal_entity,
                project=project_entity
            )
            work_projects.append(work_project)
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            path_params={
                'project_id': project_id,
                'page': page,
                'page_size': page_size
            }
        )
        
        # Mock responses
        self.mock_find_project_fiscal_case.find.return_value = Mock()
        self.mock_get_work_projects_case.get_by_fiscal_mobile.return_value = {
            'total': 3,
            'data': work_projects
        }
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['total'] == 3
        assert len(result.body['content']) == 3
        
        # Verificar se os dados estão corretos
        for i, work_project_data in enumerate(result.body['content']):
            assert work_project_data['id'] == i+1
            assert work_project_data['title'] == f"Work Project {i+1}"
            assert work_project_data['fiscal']['id'] == fiscal_id
            assert work_project_data['project']['id'] == project_id 