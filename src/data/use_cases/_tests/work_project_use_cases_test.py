import pytest
from unittest.mock import MagicMock
from datetime import datetime
from src.data.use_cases.insert_work_project import InsertWorkProject
from src.data.use_cases.get_work_project import GetWorkProject
from src.data.use_cases.get_all_work_projects import GetAllWorkProjects
from src.data.use_cases.get_work_projects_by_project import GetWorkProjectsByProject
from src.data.use_cases.get_work_projects_by_fiscal import GetWorkProjectsByFiscal
from src.data.use_cases.get_work_projects_by_project_and_fiscal import GetWorkProjectsByProjectAndFiscal
from src.data.use_cases.get_work_project_by_title import GetWorkProjectByTitle
from src.data.use_cases.count_work_projects import CountWorkProjects
from src.data.use_cases.get_work_projects_with_pagination import GetWorkProjectsWithPagination
from src.data.use_cases.update_work_project import UpdateWorkProject
from src.data.use_cases.delete_work_project import DeleteWorkProject
from src.domain.entities.work_project import WorkProjectEntity

@pytest.fixture
def mock_repository():
    return MagicMock()

def test_insert_work_project_calls_repository(mock_repository):
    use_case = InsertWorkProject(mock_repository)
    use_case.insert(1, 2, 'title', 'desc', 'photo.png')
    mock_repository.insert.assert_called_once_with(
        project_id=1, fiscal_id=2, title='title', description='desc', photo_name='photo.png', additional_documents=None
    )

def test_get_work_project_calls_repository_and_returns_entity(mock_repository):
    entity = WorkProjectEntity(
        id=1, project_id=1, fiscal_id=2, title='t', description='d', photo_name='p',
        additional_documents=None, created_at=datetime.now(), updated_at=datetime.now()
    )
    mock_repository.find.return_value = entity
    use_case = GetWorkProject(mock_repository)
    result = use_case.get(1)
    mock_repository.find.assert_called_once_with(work_project_id=1)
    assert result == entity

def test_get_all_work_projects_calls_repository_and_returns_list(mock_repository):
    entities = [MagicMock(), MagicMock()]
    mock_repository.find_all.return_value = entities
    use_case = GetAllWorkProjects(mock_repository)
    result = use_case.get_all()
    mock_repository.find_all.assert_called_once()
    assert result == entities

def test_get_work_projects_by_project_calls_repository_and_returns_list(mock_repository):
    entities = [MagicMock()]
    mock_repository.find_by_project.return_value = entities
    use_case = GetWorkProjectsByProject(mock_repository)
    result = use_case.get_by_project(10)
    mock_repository.find_by_project.assert_called_once_with(project_id=10)
    assert result == entities

def test_get_work_projects_by_fiscal_calls_repository_and_returns_list(mock_repository):
    entities = [MagicMock()]
    mock_repository.find_by_fiscal.return_value = entities
    use_case = GetWorkProjectsByFiscal(mock_repository)
    result = use_case.get_by_fiscal(20)
    mock_repository.find_by_fiscal.assert_called_once_with(fiscal_id=20)
    assert result == entities

def test_get_work_projects_by_project_and_fiscal_calls_repository_and_returns_list(mock_repository):
    entities = [MagicMock()]
    mock_repository.find_by_project_and_fiscal.return_value = entities
    use_case = GetWorkProjectsByProjectAndFiscal(mock_repository)
    result = use_case.get_by_project_and_fiscal(1, 2)
    mock_repository.find_by_project_and_fiscal.assert_called_once_with(project_id=1, fiscal_id=2)
    assert result == entities

def test_get_work_project_by_title_calls_repository_and_returns_entity(mock_repository):
    entity = MagicMock()
    mock_repository.find_by_title.return_value = entity
    use_case = GetWorkProjectByTitle(mock_repository)
    result = use_case.get_by_title('titulo')
    mock_repository.find_by_title.assert_called_once_with(title='titulo')
    assert result == entity

def test_count_work_projects_calls_repository_and_returns_dict(mock_repository):
    count_dict = {'count': 5}
    mock_repository.count_work_projects.return_value = count_dict
    use_case = CountWorkProjects(mock_repository)
    result = use_case.count()
    mock_repository.count_work_projects.assert_called_once()
    assert result == count_dict

def test_get_work_projects_with_pagination_calls_repository_and_returns_dict(mock_repository):
    paginated = {'total': 2, 'items': [MagicMock()]}
    mock_repository.get_work_projects_with_pagination.return_value = paginated
    use_case = GetWorkProjectsWithPagination(mock_repository)
    result = use_case.get_with_pagination(1, 10)
    mock_repository.get_work_projects_with_pagination.assert_called_once_with(page=1, page_size=10)
    assert result == paginated

def test_update_work_project_calls_repository(mock_repository):
    use_case = UpdateWorkProject(mock_repository)
    params = {'title': 'novo'}
    use_case.update(1, params)
    mock_repository.update.assert_called_once_with(work_project_id=1, update_params=params)

def test_delete_work_project_calls_repository(mock_repository):
    use_case = DeleteWorkProject(mock_repository)
    use_case.delete(99)
    mock_repository.delete.assert_called_once_with(work_project_id=99)