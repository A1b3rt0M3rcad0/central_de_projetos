import pytest
from unittest.mock import Mock
from src.data.use_cases.update_work_project_title import UpdateWorkProjectTitle

class TestUpdateWorkProjectTitle:
    
    def test_update_work_project_title_success(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectTitle(mock_repository)
        work_project_id = 1
        title = "Novo Título do Projeto"
        
        # Act
        use_case.update(work_project_id, title)
        
        # Assert
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"title": title}
        )
    
    def test_update_work_project_title_empty_string_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectTitle(mock_repository)
        work_project_id = 1
        title = ""
        
        # Act & Assert
        with pytest.raises(ValueError, match="Title cannot be empty"):
            use_case.update(work_project_id, title)
        
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_title_whitespace_only_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectTitle(mock_repository)
        work_project_id = 1
        title = "   "
        
        # Act & Assert
        with pytest.raises(ValueError, match="Title cannot be empty"):
            use_case.update(work_project_id, title)
        
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_title_none_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectTitle(mock_repository)
        work_project_id = 1
        title = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Title cannot be empty"):
            use_case.update(work_project_id, title)
        
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_title_strips_whitespace(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectTitle(mock_repository)
        work_project_id = 1
        title = "  Título com Espaços  "
        
        # Act
        use_case.update(work_project_id, title)
        
        # Assert
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"title": "Título com Espaços"}
        ) 