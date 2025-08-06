#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.verify_fiscal_work_project_association import VerifyFiscalWorkProjectAssociation
from src.domain.entities.work_project import WorkProjectEntity
from datetime import datetime

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def work_project_entity():
    return WorkProjectEntity(
        id=1,
        project_id=1,
        fiscal_id=123,
        title="Test Project",
        description="Test Description",
        photo_name="test.jpg",
        additional_documents=None,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

def test_verify_fiscal_work_project_association_success(mock_repository, work_project_entity):
    """Testa verificação bem-sucedida de associação fiscal-work_project"""
    mock_repository.find.return_value = work_project_entity
    use_case = VerifyFiscalWorkProjectAssociation(mock_repository)
    
    result = use_case.verify(fiscal_id=123, work_project_id=1)
    
    mock_repository.find.assert_called_once_with(1)
    assert result is True

def test_verify_fiscal_work_project_association_wrong_fiscal(mock_repository, work_project_entity):
    """Testa verificação quando fiscal_id não corresponde"""
    mock_repository.find.return_value = work_project_entity
    use_case = VerifyFiscalWorkProjectAssociation(mock_repository)
    
    result = use_case.verify(fiscal_id=456, work_project_id=1)
    
    mock_repository.find.assert_called_once_with(1)
    assert result is False

def test_verify_fiscal_work_project_association_work_project_not_found(mock_repository):
    """Testa verificação quando work_project não é encontrado"""
    mock_repository.find.side_effect = Exception("Work project not found")
    use_case = VerifyFiscalWorkProjectAssociation(mock_repository)
    
    result = use_case.verify(fiscal_id=123, work_project_id=999)
    
    mock_repository.find.assert_called_once_with(999)
    assert result is False

def test_verify_fiscal_work_project_association_repository_error(mock_repository):
    """Testa verificação quando repositório lança exceção"""
    mock_repository.find.side_effect = Exception("Database error")
    use_case = VerifyFiscalWorkProjectAssociation(mock_repository)
    
    result = use_case.verify(fiscal_id=123, work_project_id=1)
    
    mock_repository.find.assert_called_once_with(1)
    assert result is False 