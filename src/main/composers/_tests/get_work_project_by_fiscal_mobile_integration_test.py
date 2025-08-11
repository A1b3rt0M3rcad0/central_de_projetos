#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.main.composers.get_work_project_by_fiscal_mobile_composer import get_work_project_by_fiscal_mobile_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime


class TestGetWorkProjectByFiscalMobileIntegration:

    def test_integration_with_real_entities(self):
        """Testa a integração com entidades reais"""
        # Arrange
        # Criar entidades reais para o teste
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
        
        # Mock do repositório
        with patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.find_by_fiscal_and_id.return_value = work_project_entity
            mock_repo_class.return_value = mock_repo
            
            # Act
            handler = get_work_project_by_fiscal_mobile_composer()
            http_request = HttpRequest(
                body={
                    'work_project_id': 1,
                    'fiscal_id': 1
                }
            )
            result = handler(http_request)
            
            # Assert
            assert isinstance(result, HttpResponse)
            assert result.status_code == 200
            assert result.body['message'] == 'Work Project found successfully'
            assert result.body['content']['id'] == 1
            assert result.body['content']['title'] == 'Test Work Project'
            assert result.body['content']['fiscal']['name'] == 'Test Fiscal'
            assert result.body['content']['project']['name'] == 'Test Project'

    def test_integration_with_work_project_not_found(self):
        """Testa a integração quando o work project não é encontrado"""
        # Arrange
        from src.errors.repository.not_exists_error.work_project_not_exists import WorkProjectNotExists
        
        # Mock do repositório
        with patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.find_by_fiscal_and_id.side_effect = WorkProjectNotExists(
                message="WorkProject with id: 999 does not exists or fiscal 1 is not associated"
            )
            mock_repo_class.return_value = mock_repo
            
            # Act & Assert
            handler = get_work_project_by_fiscal_mobile_composer()
            http_request = HttpRequest(
                body={
                    'work_project_id': 999,
                    'fiscal_id': 1
                }
            )
            
            with pytest.raises(WorkProjectNotExists):
                handler(http_request)

    def test_integration_with_database_error(self):
        """Testa a integração quando há erro no banco de dados"""
        # Arrange
        from src.errors.repository.error_on_find.error_on_find_work_project import ErrorOnFindWorkProject
        
        # Mock do repositório
        with patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.find_by_fiscal_and_id.side_effect = ErrorOnFindWorkProject(
                message="Database connection error"
            )
            mock_repo_class.return_value = mock_repo
            
            # Act & Assert
            handler = get_work_project_by_fiscal_mobile_composer()
            http_request = HttpRequest(
                body={
                    'work_project_id': 1,
                    'fiscal_id': 1
                }
            )
            
            with pytest.raises(ErrorOnFindWorkProject):
                handler(http_request)

    def test_integration_with_fiscal_not_associated(self):
        """Testa a integração quando o fiscal não está associado ao work project"""
        # Arrange
        from src.errors.repository.not_exists_error.work_project_not_exists import WorkProjectNotExists
        
        # Mock do repositório
        with patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.find_by_fiscal_and_id.side_effect = WorkProjectNotExists(
                message="WorkProject with id: 1 does not exists or fiscal 999 is not associated"
            )
            mock_repo_class.return_value = mock_repo
            
            # Act & Assert
            handler = get_work_project_by_fiscal_mobile_composer()
            http_request = HttpRequest(
                body={
                    'work_project_id': 1,
                    'fiscal_id': 999  # Fiscal não associado
                }
            )
            
            with pytest.raises(WorkProjectNotExists):
                handler(http_request)

    def test_integration_with_complete_work_project_data(self):
        """Testa a integração com dados completos do work project"""
        # Arrange
        fiscal_entity = FiscalEntity(
            fiscal_id=1,
            name="Complete Test Fiscal",
            created_at=datetime.now()
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
        
        # Mock do repositório
        with patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.find_by_fiscal_and_id.return_value = work_project_entity
            mock_repo_class.return_value = mock_repo
            
            # Act
            handler = get_work_project_by_fiscal_mobile_composer()
            http_request = HttpRequest(
                body={
                    'work_project_id': 1,
                    'fiscal_id': 1
                }
            )
            result = handler(http_request)
            
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