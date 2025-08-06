#pylint:disable=all
import pytest
from unittest.mock import MagicMock
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.data.use_cases.update_status_from_project import UpdateStatusFromProject
from src.errors.repository.not_exists_error.project_not_exists import ProjectNotExistsError
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError

@pytest.fixture
def mock_history_project_repository():
    return MagicMock()

@pytest.fixture
def mock_project_repository():
    return MagicMock()

# Testes para CreateHistoryProject
def test_create_history_project_success(mock_history_project_repository):
    """Testa criação de histórico de projeto com sucesso"""
    use_case = CreateHistoryProject(mock_history_project_repository)
    
    use_case.create(
        project_id=1,
        data_name="Atualização de Status",
        description="Status alterado para Em Andamento"
    )
    
    mock_history_project_repository.insert.assert_called_once_with(
        project_id=1,
        data_name="Atualização de Status",
        description="Status alterado para Em Andamento"
    )

def test_create_history_project_without_description(mock_history_project_repository):
    """Testa criação de histórico de projeto sem descrição"""
    use_case = CreateHistoryProject(mock_history_project_repository)
    
    use_case.create(
        project_id=1,
        data_name="Criação de Projeto"
    )
    
    mock_history_project_repository.insert.assert_called_once_with(
        project_id=1,
        data_name="Criação de Projeto",
        description=None
    )

def test_create_history_project_project_not_exists(mock_history_project_repository):
    """Testa criação de histórico quando projeto não existe"""
    mock_history_project_repository.insert.side_effect = ProjectNotExistsError("Projeto não existe")
    use_case = CreateHistoryProject(mock_history_project_repository)
    
    with pytest.raises(ProjectNotFoundError):
        use_case.create(
            project_id=999,
            data_name="Atualização de Status",
            description="Status alterado"
        )

def test_create_history_project_repository_error(mock_history_project_repository):
    """Testa criação de histórico quando repositório lança exceção"""
    mock_history_project_repository.insert.side_effect = Exception("Erro no repositório")
    use_case = CreateHistoryProject(mock_history_project_repository)
    
    with pytest.raises(Exception):
        use_case.create(
            project_id=1,
            data_name="Atualização de Status",
            description="Status alterado"
        )

# Testes para UpdateStatusFromProject
def test_update_status_from_project_success(mock_project_repository):
    """Testa atualização de status de projeto com sucesso"""
    use_case = UpdateStatusFromProject(mock_project_repository)
    
    use_case.update(project_id=1, status_id=2)
    
    mock_project_repository.update.assert_called_once_with(
        project_id=1,
        update_params={'status_id': 2}
    )

def test_update_status_from_project_repository_error(mock_project_repository):
    """Testa atualização de status quando repositório lança exceção"""
    mock_project_repository.update.side_effect = Exception("Erro no repositório")
    use_case = UpdateStatusFromProject(mock_project_repository)
    
    with pytest.raises(Exception):
        use_case.update(project_id=1, status_id=2)

def test_update_status_from_project_same_status(mock_project_repository):
    """Testa atualização de status para o mesmo status"""
    use_case = UpdateStatusFromProject(mock_project_repository)
    
    use_case.update(project_id=1, status_id=1)
    
    mock_project_repository.update.assert_called_once_with(
        project_id=1,
        update_params={'status_id': 1}
    )

def test_update_status_from_project_invalid_status_id(mock_project_repository):
    """Testa atualização de status com ID inválido"""
    use_case = UpdateStatusFromProject(mock_project_repository)
    
    use_case.update(project_id=1, status_id=999)
    
    mock_project_repository.update.assert_called_once_with(
        project_id=1,
        update_params={'status_id': 999}
    ) 