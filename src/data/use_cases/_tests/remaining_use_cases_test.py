import pytest
from unittest.mock import MagicMock
from src.data.use_cases.delete_fiscal_from_project import DeleteFiscalFromProject
from src.data.use_cases.update_status_description import UpdateStatusDescription
from src.data.use_cases.delete_all_documents_from_project import DeleteAllDocumentsFromProject
from src.data.use_cases.get_document import GetDocument
from src.domain.value_objects.document import Document
from src.errors.use_cases.status_description_error import StatusDescriptionError
from src.errors.use_cases.document_not_found_error import DocumentNotFoundError
from src.errors.repository.already_exists_error.status_already_exists import StatusAlreadyExists

@pytest.fixture
def mock_project_fiscal_repository():
    return MagicMock()

@pytest.fixture
def mock_status_repository():
    return MagicMock()

@pytest.fixture
def mock_project_document_repository():
    return MagicMock()

@pytest.fixture
def mock_document():
    return MagicMock()

def test_delete_fiscal_from_project_success(mock_project_fiscal_repository):
    use_case = DeleteFiscalFromProject(mock_project_fiscal_repository)
    use_case.delete(1)
    
    mock_project_fiscal_repository.delete_all_from_project.assert_called_once_with(project_id=1)

def test_delete_fiscal_from_project_repository_error(mock_project_fiscal_repository):
    mock_project_fiscal_repository.delete_all_from_project.side_effect = Exception("Repository error")
    
    use_case = DeleteFiscalFromProject(mock_project_fiscal_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1)

def test_update_status_description_success(mock_status_repository):
    use_case = UpdateStatusDescription(mock_status_repository)
    use_case.update(1, "New Description")
    
    mock_status_repository.update.assert_called_once_with(status_id=1, new_description="New Description")

def test_update_status_description_status_already_exists(mock_status_repository):
    mock_status_repository.update.side_effect = StatusAlreadyExists("Status already exists")
    
    use_case = UpdateStatusDescription(mock_status_repository)
    
    with pytest.raises(StatusDescriptionError, match="Error on update status description"):
        use_case.update(1, "New Description")

def test_update_status_description_repository_error(mock_status_repository):
    mock_status_repository.update.side_effect = Exception("Repository error")
    
    use_case = UpdateStatusDescription(mock_status_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.update(1, "New Description")

def test_delete_all_documents_from_project_success(mock_project_document_repository):
    use_case = DeleteAllDocumentsFromProject(mock_project_document_repository)
    use_case.delete(1)
    
    mock_project_document_repository.delete_project.assert_called_once_with(project_id=1)

def test_delete_all_documents_from_project_repository_error(mock_project_document_repository):
    mock_project_document_repository.delete_project.side_effect = Exception("Repository error")
    
    use_case = DeleteAllDocumentsFromProject(mock_project_document_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.delete(1)

def test_get_document_success(mock_project_document_repository, mock_document):
    mock_project_document_repository.get_document.return_value = mock_document
    
    use_case = GetDocument(mock_project_document_repository)
    result = use_case.document(1, "test.pdf")
    
    mock_project_document_repository.get_document.assert_called_once_with(
        project_id=1, 
        document_name="test.pdf", 
        _document_class=Document
    )
    assert result == mock_document

def test_get_document_with_custom_document_class(mock_project_document_repository, mock_document):
    class CustomDocument(Document):
        pass
    
    mock_project_document_repository.get_document.return_value = mock_document
    
    use_case = GetDocument(mock_project_document_repository)
    result = use_case.document(1, "test.pdf", CustomDocument)
    
    mock_project_document_repository.get_document.assert_called_once_with(
        project_id=1, 
        document_name="test.pdf", 
        _document_class=CustomDocument
    )
    assert result == mock_document

def test_get_document_not_found(mock_project_document_repository):
    mock_project_document_repository.get_document.side_effect = AttributeError("Document not found")
    
    use_case = GetDocument(mock_project_document_repository)
    
    with pytest.raises(DocumentNotFoundError, match='Document "test.pdf" not found in project "id:1"'):
        use_case.document(1, "test.pdf")

def test_get_document_repository_error(mock_project_document_repository):
    mock_project_document_repository.get_document.side_effect = Exception("Repository error")
    
    use_case = GetDocument(mock_project_document_repository)
    
    with pytest.raises(Exception, match="Repository error"):
        use_case.document(1, "test.pdf") 