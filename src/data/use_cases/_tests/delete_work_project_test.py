import pytest
#pylint:disable=W0611,W0201
from unittest.mock import Mock, patch
from src.data.use_cases.delete_work_project import DeleteWorkProject
from src.domain.entities.work_project import WorkProjectEntity
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity
from src.domain.value_objects.monetary_value import MonetaryValue
from src.errors.use_cases.delete_work_project_error import DeleteWorkProjectError
from src.errors.repository.not_exists_error.work_project_not_exists import WorkProjectNotExists
from datetime import datetime

class TestDeleteWorkProject:
    
    def setup_method(self):
        self.mock_work_project_repository = Mock()
        self.mock_project_document_fiscal_repository = Mock()
        self.delete_work_project = DeleteWorkProject(
            work_project_repository=self.mock_work_project_repository,
            project_document_fiscal_repository=self.mock_project_document_fiscal_repository
        )
    
    def test_delete_work_project_success(self):
        """Testa a deleção bem-sucedida de um work project"""
        # Arrange
        work_project_id = 1
        fiscal_id = 123
        
        # Mock do work project retornado
        mock_work_project = WorkProjectEntity(
            id=work_project_id,
            project_id=1,
            fiscal_id=fiscal_id,
            title="Test Work Project",
            description="Test Description",
            photo_name="test.jpg",
            additional_documents=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            fiscal=FiscalEntity(
                fiscal_id=fiscal_id,
                name="Test Fiscal",
                created_at=datetime.now()
            ),
            project=ProjectEntity(
                project_id=1,
                status_id=1,
                name="Test Project",
                andamento_do_projeto="Em andamento",
                verba_disponivel=MonetaryValue(1000.0),
                start_date=datetime.now(),
                expected_completion_date=datetime.now(),
                end_date=None
            )
        )
        
        self.mock_work_project_repository.find.return_value = mock_work_project
        self.mock_work_project_repository.delete.return_value = None
        self.mock_project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project.return_value = None
        
        # Act
        self.delete_work_project.delete(work_project_id)
        
        # Assert
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id
        )
        self.mock_work_project_repository.delete.assert_called_once_with(work_project_id=work_project_id)
    
    def test_delete_work_project_not_found(self):
        """Testa a deleção quando o work project não existe"""
        # Arrange
        work_project_id = 999
        
        self.mock_work_project_repository.find.side_effect = WorkProjectNotExists(
            message=f'WorkProject with id: {work_project_id} does not exists'
        )
        
        # Act & Assert
        with pytest.raises(DeleteWorkProjectError) as exc_info:
            self.delete_work_project.delete(work_project_id)
        
        assert "Erro ao deletar work project" in str(exc_info.value)
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project.assert_not_called()
        self.mock_work_project_repository.delete.assert_not_called()
    
    def test_delete_work_project_document_deletion_error(self):
        """Testa erro na deleção dos documentos"""
        # Arrange
        work_project_id = 1
        fiscal_id = 123
        
        mock_work_project = WorkProjectEntity(
            id=work_project_id,
            project_id=1,
            fiscal_id=fiscal_id,
            title="Test Work Project",
            description="Test Description",
            photo_name="test.jpg",
            additional_documents=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            fiscal=FiscalEntity(
                fiscal_id=fiscal_id,
                name="Test Fiscal",
                created_at=datetime.now()
            ),
            project=ProjectEntity(
                project_id=1,
                status_id=1,
                name="Test Project",
                andamento_do_projeto="Em andamento",
                verba_disponivel=MonetaryValue(1000.0),
                start_date=datetime.now(),
                expected_completion_date=datetime.now(),
                end_date=None
            )
        )
        
        self.mock_work_project_repository.find.return_value = mock_work_project
        self.mock_project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project.side_effect = Exception("Document deletion error")
        
        # Act & Assert
        with pytest.raises(DeleteWorkProjectError) as exc_info:
            self.delete_work_project.delete(work_project_id)
        
        assert "Erro ao deletar work project" in str(exc_info.value)
        assert "Document deletion error" in str(exc_info.value)
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id
        )
        self.mock_work_project_repository.delete.assert_not_called()
    
    def test_delete_work_project_repository_deletion_error(self):
        """Testa erro na deleção do work project no repositório"""
        # Arrange
        work_project_id = 1
        fiscal_id = 123
        
        mock_work_project = WorkProjectEntity(
            id=work_project_id,
            project_id=1,
            fiscal_id=fiscal_id,
            title="Test Work Project",
            description="Test Description",
            photo_name="test.jpg",
            additional_documents=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            fiscal=FiscalEntity(
                fiscal_id=fiscal_id,
                name="Test Fiscal",
                created_at=datetime.now()
            ),
            project=ProjectEntity(
                project_id=1,
                status_id=1,
                name="Test Project",
                andamento_do_projeto="Em andamento",
                verba_disponivel=MonetaryValue(1000.0),
                start_date=datetime.now(),
                expected_completion_date=datetime.now(),
                end_date=None
            )
        )
        
        self.mock_work_project_repository.find.return_value = mock_work_project
        self.mock_project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project.return_value = None
        self.mock_work_project_repository.delete.side_effect = Exception("Repository deletion error")
        
        # Act & Assert
        with pytest.raises(DeleteWorkProjectError) as exc_info:
            self.delete_work_project.delete(work_project_id)
        
        assert "Erro ao deletar work project" in str(exc_info.value)
        assert "Repository deletion error" in str(exc_info.value)
        self.mock_work_project_repository.find.assert_called_once_with(work_project_id)
        self.mock_project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project.assert_called_once_with(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id
        )
        self.mock_work_project_repository.delete.assert_called_once_with(work_project_id=work_project_id) 