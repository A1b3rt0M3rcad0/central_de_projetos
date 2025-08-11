#pylint:disable=all
import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime, timezone
from src.data.use_cases.get_work_projects_by_fiscal_mobile import GetWorkProjectsByFiscalMobile
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue


class TestGetWorkProjectsByFiscalMobile:

    def setup_method(self):
        """Setup para cada teste"""
        self.mock_work_project_repository = Mock()
        self.use_case = GetWorkProjectsByFiscalMobile(
            work_project_repository=self.mock_work_project_repository
        )

    def test_get_by_fiscal_mobile_success(self):
        """Testa o sucesso da busca de work projects"""
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
        
        # Mock work project entities
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
        
        # Mock repository response
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal_and_project.return_value = {
            'total': 3,
            'data': work_projects
        }
        
        # Act
        result = self.use_case.get_by_fiscal_mobile(
            fiscal_id=fiscal_id,
            project_id=project_id,
            page=page,
            page_size=page_size
        )
        
        # Assert
        assert result['total'] == 3
        assert len(result['data']) == 3
        assert result['data'] == work_projects
        
        # Verificar se o repository foi chamado corretamente
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal_and_project.assert_called_once_with(
            fiscal_id=fiscal_id,
            project_id=project_id,
            page=page,
            page_size=page_size
        )

    def test_get_by_fiscal_mobile_empty_list(self):
        """Testa quando não há work projects"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        page = 1
        page_size = 10
        
        # Mock repository response vazio
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal_and_project.return_value = {
            'total': 0,
            'data': []
        }
        
        # Act
        result = self.use_case.get_by_fiscal_mobile(
            fiscal_id=fiscal_id,
            project_id=project_id,
            page=page,
            page_size=page_size
        )
        
        # Assert
        assert result['total'] == 0
        assert len(result['data']) == 0
        assert result['data'] == []

    def test_get_by_fiscal_mobile_pagination_first_page(self):
        """Testa paginação na primeira página"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        page = 1
        page_size = 2
        
        # Criar 5 work projects
        work_projects = []
        for i in range(5):
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
                fiscal=Mock(),
                project=Mock()
            )
            work_projects.append(work_project)
        
        # Mock repository response
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal_and_project.return_value = {
            'total': 5,
            'data': work_projects[:2]  # Primeira página
        }
        
        # Act
        result = self.use_case.get_by_fiscal_mobile(
            fiscal_id=fiscal_id,
            project_id=project_id,
            page=page,
            page_size=page_size
        )
        
        # Assert
        assert result['total'] == 5
        assert len(result['data']) == 2  # page_size = 2
        assert result['data'][0].id == 1
        assert result['data'][1].id == 2

    def test_get_by_fiscal_mobile_pagination_second_page(self):
        """Testa paginação na segunda página"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        page = 2
        page_size = 2
        
        # Criar 5 work projects
        work_projects = []
        for i in range(5):
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
                fiscal=Mock(),
                project=Mock()
            )
            work_projects.append(work_project)
        
        # Mock repository response
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal_and_project.return_value = {
            'total': 5,
            'data': work_projects[2:4]  # Segunda página
        }
        
        # Act
        result = self.use_case.get_by_fiscal_mobile(
            fiscal_id=fiscal_id,
            project_id=project_id,
            page=page,
            page_size=page_size
        )
        
        # Assert
        assert result['total'] == 5
        assert len(result['data']) == 2  # page_size = 2
        assert result['data'][0].id == 3
        assert result['data'][1].id == 4

    def test_get_by_fiscal_mobile_pagination_last_page(self):
        """Testa paginação na última página"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        page = 3
        page_size = 2
        
        # Criar 5 work projects
        work_projects = []
        for i in range(5):
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
                fiscal=Mock(),
                project=Mock()
            )
            work_projects.append(work_project)
        
        # Mock repository response
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal_and_project.return_value = {
            'total': 5,
            'data': work_projects[4:5]  # Última página
        }
        
        # Act
        result = self.use_case.get_by_fiscal_mobile(
            fiscal_id=fiscal_id,
            project_id=project_id,
            page=page,
            page_size=page_size
        )
        
        # Assert
        assert result['total'] == 5
        assert len(result['data']) == 1  # Último item
        assert result['data'][0].id == 5

    def test_get_by_fiscal_mobile_pagination_page_out_of_range(self):
        """Testa paginação quando a página está fora do range"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        page = 10  # Página inexistente
        page_size = 2
        
        # Criar 5 work projects
        work_projects = []
        for i in range(5):
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
                fiscal=Mock(),
                project=Mock()
            )
            work_projects.append(work_project)
        
        # Mock repository response
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal_and_project.return_value = {
            'total': 5,
            'data': []  # Página fora do range
        }
        
        # Act
        result = self.use_case.get_by_fiscal_mobile(
            fiscal_id=fiscal_id,
            project_id=project_id,
            page=page,
            page_size=page_size
        )
        
        # Assert
        assert result['total'] == 5
        assert len(result['data']) == 0  # Lista vazia quando página não existe

    def test_get_by_fiscal_mobile_repository_exception(self):
        """Testa quando o repository lança uma exceção"""
        # Arrange
        fiscal_id = 1
        project_id = 2
        page = 1
        page_size = 10
        
        # Mock repository para lançar exceção
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal_and_project.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.use_case.get_by_fiscal_mobile(
                fiscal_id=fiscal_id,
                project_id=project_id,
                page=page,
                page_size=page_size
            )
        
        assert "Database error" in str(exc_info.value) 