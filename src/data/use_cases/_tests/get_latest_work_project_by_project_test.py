#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.data.use_cases.get_latest_work_project_by_project import GetLatestWorkProjectByProject
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime, timezone

class TestGetLatestWorkProjectByProject:
    
    def setup_method(self):
        self.mock_work_project_repository = Mock()
        self.use_case = GetLatestWorkProjectByProject(self.mock_work_project_repository)
    
    def test_get_latest_by_project_success(self):
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
        
        self.mock_work_project_repository.find_latest_by_project.return_value = work_project_entity
        
        # Act
        result = self.use_case.get_latest_by_project(project_id=project_id)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert result.project_id == project_id
        assert result.title == "Trabalho Mais Recente"
        assert result.description == "Descrição do trabalho mais recente"
        assert result.photo_name == "foto_recente.jpg"
        assert result.fiscal is not None
        assert result.fiscal.name == "Fiscal Teste"
        assert result.project is not None
        assert result.project.name == "Projeto Teste"
        
        self.mock_work_project_repository.find_latest_by_project.assert_called_once_with(project_id=project_id)
    
    def test_get_latest_by_project_no_work_projects(self):
        # Arrange
        project_id = 1
        self.mock_work_project_repository.find_latest_by_project.return_value = None
        
        # Act
        result = self.use_case.get_latest_by_project(project_id=project_id)
        
        # Assert
        assert result is None
        self.mock_work_project_repository.find_latest_by_project.assert_called_once_with(project_id=project_id)
    
    def test_get_latest_by_project_repository_error(self):
        # Arrange
        project_id = 1
        self.mock_work_project_repository.find_latest_by_project.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            self.use_case.get_latest_by_project(project_id=project_id)
        
        self.mock_work_project_repository.find_latest_by_project.assert_called_once_with(project_id=project_id) 