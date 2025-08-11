#pylint:disable=all
import pytest
from unittest.mock import Mock
from src.data.use_cases.get_work_project_by_fiscal import GetWorkProjectByFiscal
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime


class TestGetWorkProjectByFiscal:

    def test_use_case_initialization(self):
        """Testa se o use case é inicializado corretamente"""
        # Arrange
        mock_repository = Mock()
        
        # Act
        use_case = GetWorkProjectByFiscal(
            work_project_repository=mock_repository
        )
        
        # Assert
        assert use_case is not None
        assert hasattr(use_case, '_GetWorkProjectByFiscal__work_project_repository')

    def test_get_with_valid_data(self):
        """Testa o método get com dados válidos"""
        # Arrange
        mock_repository = Mock()
        
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
        
        mock_repository.find_by_fiscal_and_id.return_value = work_project_entity
        
        use_case = GetWorkProjectByFiscal(
            work_project_repository=mock_repository
        )
        
        # Act
        result = use_case.get(
            work_project_id=1,
            fiscal_id=1
        )
        
        # Assert
        assert isinstance(result, WorkProjectEntity)
        assert result.id == 1
        assert result.title == "Test Work Project"
        assert result.fiscal.name == "Test Fiscal"
        assert result.project.name == "Test Project"
        
        # Verifica se o repositório foi chamado com os parâmetros corretos
        mock_repository.find_by_fiscal_and_id.assert_called_once_with(
            work_project_id=1,
            fiscal_id=1
        )

    def test_get_with_repository_exception(self):
        """Testa o método get quando o repositório lança exceção"""
        # Arrange
        mock_repository = Mock()
        mock_repository.find_by_fiscal_and_id.side_effect = Exception("Repository error")
        
        use_case = GetWorkProjectByFiscal(
            work_project_repository=mock_repository
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Repository error"):
            use_case.get(
                work_project_id=1,
                fiscal_id=1
            )

    def test_get_with_work_project_not_found(self):
        """Testa o método get quando o work project não é encontrado"""
        # Arrange
        from src.errors.repository.not_exists_error.work_project_not_exists import WorkProjectNotExists
        
        mock_repository = Mock()
        mock_repository.find_by_fiscal_and_id.side_effect = WorkProjectNotExists(
            message="WorkProject with id: 999 does not exists or fiscal 1 is not associated"
        )
        
        use_case = GetWorkProjectByFiscal(
            work_project_repository=mock_repository
        )
        
        # Act & Assert
        with pytest.raises(WorkProjectNotExists):
            use_case.get(
                work_project_id=999,
                fiscal_id=1
            )

    def test_get_with_fiscal_not_associated(self):
        """Testa o método get quando o fiscal não está associado"""
        # Arrange
        from src.errors.repository.not_exists_error.work_project_not_exists import WorkProjectNotExists
        
        mock_repository = Mock()
        mock_repository.find_by_fiscal_and_id.side_effect = WorkProjectNotExists(
            message="WorkProject with id: 1 does not exists or fiscal 999 is not associated"
        )
        
        use_case = GetWorkProjectByFiscal(
            work_project_repository=mock_repository
        )
        
        # Act & Assert
        with pytest.raises(WorkProjectNotExists):
            use_case.get(
                work_project_id=1,
                fiscal_id=999
            )

    def test_get_with_database_error(self):
        """Testa o método get quando há erro no banco de dados"""
        # Arrange
        from src.errors.repository.error_on_find.error_on_find_work_project import ErrorOnFindWorkProject
        
        mock_repository = Mock()
        mock_repository.find_by_fiscal_and_id.side_effect = ErrorOnFindWorkProject(
            message="Database connection error"
        )
        
        use_case = GetWorkProjectByFiscal(
            work_project_repository=mock_repository
        )
        
        # Act & Assert
        with pytest.raises(ErrorOnFindWorkProject):
            use_case.get(
                work_project_id=1,
                fiscal_id=1
            )

    def test_get_with_complete_work_project_data(self):
        """Testa o método get com dados completos do work project"""
        # Arrange
        mock_repository = Mock()
        
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
        
        mock_repository.find_by_fiscal_and_id.return_value = work_project_entity
        
        use_case = GetWorkProjectByFiscal(
            work_project_repository=mock_repository
        )
        
        # Act
        result = use_case.get(
            work_project_id=1,
            fiscal_id=1
        )
        
        # Assert
        assert isinstance(result, WorkProjectEntity)
        assert result.id == 1
        assert result.title == "Complete Test Work Project"
        assert result.description == "Complete test description with more details"
        assert result.photo_name == "complete_test.jpg"
        assert result.additional_documents == ["doc1.pdf", "doc2.pdf"]
        assert result.fiscal.name == "Complete Test Fiscal"
        assert result.project.name == "Complete Test Project"
        assert result.project.andamento_do_projeto == "Concluído"
        assert str(result.project.verba_disponivel) == "$500000.00"

    def test_get_with_none_fiscal_and_project(self):
        """Testa o método get quando fiscal e project são None"""
        # Arrange
        mock_repository = Mock()
        
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
        
        mock_repository.find_by_fiscal_and_id.return_value = work_project_entity
        
        use_case = GetWorkProjectByFiscal(
            work_project_repository=mock_repository
        )
        
        # Act
        result = use_case.get(
            work_project_id=1,
            fiscal_id=1
        )
        
        # Assert
        assert isinstance(result, WorkProjectEntity)
        assert result.id == 1
        assert result.fiscal is None
        assert result.project is None 