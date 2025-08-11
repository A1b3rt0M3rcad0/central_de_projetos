#pylint:disable=all
import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime, timezone
from src.presentation.controllers.get_projects_by_fiscal_with_pagination_controller import GetProjectsByFiscalWithPaginationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.project_fiscal import ProjectFiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from src.errors.repository.not_exists_error.projects_from_fiscal_does_not_exists import ProjectFiscalNotExists


class TestGetProjectsByFiscalWithPaginationController:

    def setup_method(self):
        """Setup para cada teste"""
        self.mock_get_projects_by_fiscal_with_pagination = Mock()
        self.mock_find_project_case = Mock()
        
        self.controller = GetProjectsByFiscalWithPaginationController(
            get_projects_by_fiscal_with_pagination=self.mock_get_projects_by_fiscal_with_pagination,
            find_project_case=self.mock_find_project_case
        )

    def test_handle_success(self):
        """Testa o sucesso da operação com dados válidos"""
        # Arrange
        fiscal_id = 1
        page = 1
        page_size = 10
        
        # Mock project fiscal entity
        project_fiscal_entity = ProjectFiscalEntity(
            project_id=1,
            fiscal_id=fiscal_id,
            created_at=datetime.now(timezone.utc)
        )
        
        # Mock project entity
        project_entity = ProjectEntity(
            project_id=1,
            status_id=1,
            name="Projeto Teste",
            andamento_do_projeto="Em andamento",
            verba_disponivel=MonetaryValue(1000.0),
            start_date=datetime.now(timezone.utc),
            expected_completion_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc)
        )
        
        # Mock HTTP request
        http_request = HttpRequest(
            body={
                'fiscal_id': fiscal_id,
                'page': page,
                'page_size': page_size
            }
        )
        
        # Mock responses
        self.mock_get_projects_by_fiscal_with_pagination.get.return_value = {
            'page': page,
            'page_size': page_size,
            'total_items': 1,
            'total_pages': 1,
            'projects': [project_fiscal_entity]
        }
        self.mock_find_project_case.find.return_value = project_entity
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['message'] == 'Projects Founded'
        assert result.body['page'] == page
        assert result.body['page_size'] == page_size
        assert result.body['total_items'] == 1
        assert result.body['total_pages'] == 1
        assert len(result.body['content']) == 1
        
        # Verificar se os métodos foram chamados corretamente
        self.mock_get_projects_by_fiscal_with_pagination.get.assert_called_once_with(
            fiscal_id=fiscal_id, page=page, page_size=page_size
        )
        self.mock_find_project_case.find.assert_called_once_with(project_id=1)
        
        # Verificar conteúdo do projeto
        project_data = result.body['content'][0]
        assert project_data['id'] == 1
        assert project_data['status_id'] == 1
        assert project_data['name'] == "Projeto Teste"
        assert project_data['andamento_do_projeto'] == "Em andamento"
        assert project_data['verba_disponivel'] == 1000.0

    def test_handle_multiple_projects(self):
        """Testa o sucesso da operação com múltiplos projetos"""
        # Arrange
        fiscal_id = 1
        page = 1
        page_size = 10
        
        # Mock project fiscal entities
        project_fiscal_entities = [
            ProjectFiscalEntity(project_id=i, fiscal_id=fiscal_id, created_at=datetime.now(timezone.utc))
            for i in range(1, 4)
        ]
        
        # Mock project entities
        project_entities = [
            ProjectEntity(
                project_id=i,
                status_id=1,
                name=f"Projeto {i}",
                andamento_do_projeto=f"Andamento {i}",
                verba_disponivel=MonetaryValue(1000.0 * i),
                start_date=datetime.now(timezone.utc),
                expected_completion_date=datetime.now(timezone.utc),
                end_date=datetime.now(timezone.utc)
            )
            for i in range(1, 4)
        ]
        
        # Mock HTTP request
        http_request = HttpRequest(
            body={
                'fiscal_id': fiscal_id,
                'page': page,
                'page_size': page_size
            }
        )
        
        # Mock responses
        self.mock_get_projects_by_fiscal_with_pagination.get.return_value = {
            'page': page,
            'page_size': page_size,
            'total_items': 3,
            'total_pages': 1,
            'projects': project_fiscal_entities
        }
        
        # Mock find_project_case para retornar projetos diferentes
        self.mock_find_project_case.find.side_effect = project_entities
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['message'] == 'Projects Founded'
        assert result.body['page'] == page
        assert result.body['page_size'] == page_size
        assert result.body['total_items'] == 3
        assert result.body['total_pages'] == 1
        assert len(result.body['content']) == 3
        
        # Verificar se os métodos foram chamados corretamente
        self.mock_get_projects_by_fiscal_with_pagination.get.assert_called_once_with(
            fiscal_id=fiscal_id, page=page, page_size=page_size
        )
        assert self.mock_find_project_case.find.call_count == 3
        
        # Verificar conteúdo dos projetos
        for i, project_data in enumerate(result.body['content']):
            assert project_data['id'] == i + 1
            assert project_data['name'] == f"Projeto {i + 1}"
            assert project_data['andamento_do_projeto'] == f"Andamento {i + 1}"
            assert project_data['verba_disponivel'] == 1000.0 * (i + 1)

    def test_handle_empty_projects_list(self):
        """Testa o sucesso da operação quando não há projetos"""
        # Arrange
        fiscal_id = 1
        page = 1
        page_size = 10
        
        # Mock HTTP request
        http_request = HttpRequest(
            body={
                'fiscal_id': fiscal_id,
                'page': page,
                'page_size': page_size
            }
        )
        
        # Mock responses
        self.mock_get_projects_by_fiscal_with_pagination.get.return_value = {
            'page': page,
            'page_size': page_size,
            'total_items': 0,
            'total_pages': 0,
            'projects': []
        }
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['message'] == 'Projects Founded'
        assert result.body['page'] == page
        assert result.body['page_size'] == page_size
        assert result.body['total_items'] == 0
        assert result.body['total_pages'] == 0
        assert len(result.body['content']) == 0
        
        # Verificar se os métodos foram chamados corretamente
        self.mock_get_projects_by_fiscal_with_pagination.get.assert_called_once_with(
            fiscal_id=fiscal_id, page=page, page_size=page_size
        )
        self.mock_find_project_case.find.assert_not_called()

    def test_handle_missing_fiscal_id(self):
        """Testa erro quando fiscal_id não está presente no request"""
        # Arrange
        http_request = HttpRequest(
            body={
                'page': 1,
                'page_size': 10
            }
        )
        
        # Act & Assert
        with pytest.raises(KeyError):
            self.controller.handle(http_request)

    def test_handle_missing_page(self):
        """Testa erro quando page não está presente no request"""
        # Arrange
        http_request = HttpRequest(
            body={
                'fiscal_id': 1,
                'page_size': 10
            }
        )
        
        # Act & Assert
        with pytest.raises(KeyError):
            self.controller.handle(http_request)

    def test_handle_missing_page_size(self):
        """Testa erro quando page_size não está presente no request"""
        # Arrange
        http_request = HttpRequest(
            body={
                'fiscal_id': 1,
                'page': 1
            }
        )
        
        # Act & Assert
        with pytest.raises(KeyError):
            self.controller.handle(http_request)

    def test_handle_repository_error(self):
        """Testa erro quando o repository lança exceção"""
        # Arrange
        fiscal_id = 1
        page = 1
        page_size = 10
        
        http_request = HttpRequest(
            body={
                'fiscal_id': fiscal_id,
                'page': page,
                'page_size': page_size
            }
        )
        
        # Mock repository error
        self.mock_get_projects_by_fiscal_with_pagination.get.side_effect = ProjectFiscalNotExists("Nenhum projeto encontrado")
        
        # Act & Assert
        with pytest.raises(ProjectFiscalNotExists):
            self.controller.handle(http_request)

    def test_handle_find_project_error(self):
        """Testa erro quando find_project_case lança exceção"""
        # Arrange
        fiscal_id = 1
        page = 1
        page_size = 10
        
        # Mock project fiscal entity
        project_fiscal_entity = ProjectFiscalEntity(
            project_id=1,
            fiscal_id=fiscal_id,
            created_at=datetime.now(timezone.utc)
        )
        
        http_request = HttpRequest(
            body={
                'fiscal_id': fiscal_id,
                'page': page,
                'page_size': page_size
            }
        )
        
        # Mock responses
        self.mock_get_projects_by_fiscal_with_pagination.get.return_value = {
            'page': page,
            'page_size': page_size,
            'total_items': 1,
            'total_pages': 1,
            'projects': [project_fiscal_entity]
        }
        self.mock_find_project_case.find.side_effect = Exception("Erro ao buscar projeto")
        
        # Act & Assert
        with pytest.raises(Exception):
            self.controller.handle(http_request) 