#pylint:disable=W0201
import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from src.data.use_cases.get_latest_work_projects_by_fiscal import GetLatestWorkProjectsByFiscal
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue

class TestGetLatestWorkProjectsByFiscal:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.mock_work_project_repository = Mock()
        self.use_case = GetLatestWorkProjectsByFiscal(self.mock_work_project_repository)
    
    def test_get_latest_by_fiscal_success(self):
        """Testa o sucesso da busca de últimos work projects"""
        # Arrange
        fiscal_id = 1
        page = 1
        page_size = 10
        start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
        
        # Mock fiscal entity
        fiscal_entity = FiscalEntity(
            fiscal_id=fiscal_id,
            name="Fiscal Teste",
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
        
        # Mock work project entities
        work_projects = []
        for i in range(3):
            work_project = WorkProjectEntity(
                id=i+1,
                project_id=1,
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
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.return_value = {
            'total': 3,
            'data': work_projects
        }
        
        # Act
        result = self.use_case.get_latest_by_fiscal(
            fiscal_id=fiscal_id,
            page=page,
            page_size=page_size,
            start_date=start_date,
            end_date=end_date
        )
        
        # Assert
        assert result['total'] == 3
        assert len(result['data']) == 3
        assert result['data'] == work_projects
        
        # Verificar se o repository foi chamado corretamente
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.assert_called_once_with(
            fiscal_id=fiscal_id,
            page=page,
            page_size=page_size,
            start_date=start_date,
            end_date=end_date
        )
    
    def test_get_latest_by_fiscal_without_date_filter(self):
        """Testa busca sem filtro de data"""
        # Arrange
        fiscal_id = 1
        page = 1
        page_size = 10
        
        # Mock work project entities
        work_projects = []
        for i in range(2):
            work_project = WorkProjectEntity(
                id=i+1,
                project_id=1,
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
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.return_value = {
            'total': 2,
            'data': work_projects
        }
        
        # Act
        result = self.use_case.get_latest_by_fiscal(
            fiscal_id=fiscal_id,
            page=page,
            page_size=page_size
        )
        
        # Assert
        assert result['total'] == 2
        assert len(result['data']) == 2
        assert result['data'] == work_projects
        
        # Verificar se o repository foi chamado corretamente
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.assert_called_once_with(
            fiscal_id=fiscal_id,
            page=page,
            page_size=page_size,
            start_date=None,
            end_date=None
        )
    
    def test_get_latest_by_fiscal_empty_list(self):
        """Testa quando não há work projects"""
        # Arrange
        fiscal_id = 1
        page = 1
        page_size = 10
        
        # Mock repository response vazio
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.return_value = {
            'total': 0,
            'data': []
        }
        
        # Act
        result = self.use_case.get_latest_by_fiscal(
            fiscal_id=fiscal_id,
            page=page,
            page_size=page_size
        )
        
        # Assert
        assert result['total'] == 0
        assert len(result['data']) == 0
        assert result['data'] == []
    
    def test_get_latest_by_fiscal_repository_exception(self):
        """Testa quando o repository lança uma exceção"""
        # Arrange
        fiscal_id = 1
        page = 1
        page_size = 10
        
        # Mock repository para lançar exceção
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.use_case.get_latest_by_fiscal(
                fiscal_id=fiscal_id,
                page=page,
                page_size=page_size
            )
        
        assert "Database error" in str(exc_info.value) 