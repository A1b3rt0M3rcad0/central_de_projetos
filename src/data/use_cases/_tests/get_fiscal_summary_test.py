#pylint:disable=all
import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from src.data.use_cases.get_fiscal_summary import GetFiscalSummary
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project_fiscal import ProjectFiscalEntity
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue

class TestGetFiscalSummary:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.mock_fiscal_repository = Mock()
        self.mock_project_fiscal_repository = Mock()
        self.mock_work_project_repository = Mock()
        self.use_case = GetFiscalSummary(
            fiscal_repository=self.mock_fiscal_repository,
            project_fiscal_repository=self.mock_project_fiscal_repository,
            work_project_repository=self.mock_work_project_repository
        )
    
    def test_get_summary_success(self):
        """Testa o sucesso da busca do resumo do fiscal"""
        # Arrange
        fiscal_id = 1
        start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
        limit = 5
        
        # Mock fiscal entity
        fiscal_entity = FiscalEntity(
            fiscal_id=fiscal_id,
            name="Fiscal Teste",
            email="fiscal@teste.com",
            phone="11999999999",
            created_at=datetime.now(timezone.utc)
        )
        
        # Mock project fiscal entities
        project_fiscals = [
            ProjectFiscalEntity(project_id=1, fiscal_id=fiscal_id, created_at=datetime.now(timezone.utc)),
            ProjectFiscalEntity(project_id=2, fiscal_id=fiscal_id, created_at=datetime.now(timezone.utc))
        ]
        
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
        
        # Mock repository responses
        self.mock_fiscal_repository.find_by_id.return_value = fiscal_entity
        self.mock_project_fiscal_repository.find_all_from_fiscal.return_value = project_fiscals
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal.return_value = {'total': 3}
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.return_value = {'total': 2, 'data': work_projects}
        self.mock_work_project_repository.find_by_fiscal.return_value = work_projects
        
        # Act
        result = self.use_case.get_summary(
            fiscal_id=fiscal_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        
        # Assert
        assert result['fiscal']['id'] == fiscal_id
        assert result['fiscal']['name'] == "Fiscal Teste"
        assert result['fiscal']['email'] == "fiscal@teste.com"
        assert result['fiscal']['phone'] == "11999999999"
        assert result['total_projetos_vinculados'] == 2
        assert result['total_fiscalizacoes'] == 3
        assert result['fiscalizacoes_no_periodo'] == 2
        assert result['documentos_enviados'] == 6  # 3 fotos + 3 documentos adicionais
        assert len(result['fiscalizacoes_por_projeto']) == 1
        assert result['fiscalizacoes_por_projeto'][0]['count'] == 3
        assert len(result['ultimas_fiscalizacoes']) == 3
        
        # Verificar se os repositories foram chamados corretamente
        self.mock_fiscal_repository.find_by_id.assert_called_once_with(fiscal_id)
        self.mock_project_fiscal_repository.find_all_from_fiscal.assert_called_once_with(fiscal_id)
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal.assert_called_once_with(
            fiscal_id=fiscal_id, page=1, page_size=1
        )
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.assert_called()
        # find_by_fiscal é chamado duas vezes: uma para calcular distribuição e outra para última atividade
        assert self.mock_work_project_repository.find_by_fiscal.call_count == 2
        self.mock_work_project_repository.find_by_fiscal.assert_any_call(fiscal_id)
    
    def test_get_summary_without_date_filter(self):
        """Testa busca sem filtro de data"""
        # Arrange
        fiscal_id = 1
        limit = 3
        
        # Mock fiscal entity
        fiscal_entity = FiscalEntity(
            fiscal_id=fiscal_id,
            name="Fiscal Teste",
            email="fiscal@teste.com",
            phone="11999999999",
            created_at=datetime.now(timezone.utc)
        )
        
        # Mock empty project fiscals
        self.mock_project_fiscal_repository.find_all_from_fiscal.side_effect = Exception("No projects")
        
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
                additional_documents=None,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                fiscal=fiscal_entity,
                project=None
            )
            work_projects.append(work_project)
        
        # Mock repository responses
        self.mock_fiscal_repository.find_by_id.return_value = fiscal_entity
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal.return_value = {'total': 2}
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.return_value = {'total': 2, 'data': work_projects}
        self.mock_work_project_repository.find_by_fiscal.return_value = work_projects
        
        # Act
        result = self.use_case.get_summary(
            fiscal_id=fiscal_id,
            start_date=None,
            end_date=None,
            limit=limit
        )
        
        # Assert
        assert result['total_projetos_vinculados'] == 0
        assert result['total_fiscalizacoes'] == 2
        assert result['fiscalizacoes_no_periodo'] == 2
        assert result['documentos_enviados'] == 2  # 2 fotos apenas
        assert len(result['ultimas_fiscalizacoes']) == 2
    
    def test_get_summary_with_custom_limit(self):
        """Testa busca com limite personalizado"""
        # Arrange
        fiscal_id = 1
        limit = 10
        
        # Mock fiscal entity
        fiscal_entity = FiscalEntity(
            fiscal_id=fiscal_id,
            name="Fiscal Teste",
            email="fiscal@teste.com",
            phone="11999999999",
            created_at=datetime.now(timezone.utc)
        )
        
        # Mock work project entities
        work_projects = []
        for i in range(5):
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
                project=None
            )
            work_projects.append(work_project)
        
        # Mock repository responses
        self.mock_fiscal_repository.find_by_id.return_value = fiscal_entity
        self.mock_project_fiscal_repository.find_all_from_fiscal.return_value = []
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal.return_value = {'total': 5}
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.return_value = {'total': 5, 'data': work_projects}
        self.mock_work_project_repository.find_by_fiscal.return_value = work_projects
        
        # Act
        result = self.use_case.get_summary(
            fiscal_id=fiscal_id,
            start_date=None,
            end_date=None,
            limit=limit
        )
        
        # Assert
        assert len(result['ultimas_fiscalizacoes']) == 5
        assert result['documentos_enviados'] == 10  # 5 fotos + 5 documentos
    
    def test_get_summary_with_no_work_projects(self):
        """Testa busca quando não há work projects"""
        # Arrange
        fiscal_id = 1
        
        # Mock fiscal entity
        fiscal_entity = FiscalEntity(
            fiscal_id=fiscal_id,
            name="Fiscal Teste",
            email="fiscal@teste.com",
            phone="11999999999",
            created_at=datetime.now(timezone.utc)
        )
        
        # Mock repository responses
        self.mock_fiscal_repository.find_by_id.return_value = fiscal_entity
        self.mock_project_fiscal_repository.find_all_from_fiscal.return_value = []
        self.mock_work_project_repository.get_work_projects_with_pagination_by_fiscal.return_value = {'total': 0}
        self.mock_work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter.return_value = {'total': 0, 'data': []}
        self.mock_work_project_repository.find_by_fiscal.return_value = []
        
        # Act
        result = self.use_case.get_summary(
            fiscal_id=fiscal_id,
            start_date=None,
            end_date=None,
            limit=5
        )
        
        # Assert
        assert result['total_projetos_vinculados'] == 0
        assert result['total_fiscalizacoes'] == 0
        assert result['fiscalizacoes_no_periodo'] == 0
        assert result['documentos_enviados'] == 0
        assert result['last_activity_at'] is None
        assert len(result['ultimas_fiscalizacoes']) == 0
        assert len(result['fiscalizacoes_por_projeto']) == 0 