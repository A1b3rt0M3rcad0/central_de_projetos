import pytest
from unittest.mock import Mock
from src.data.use_cases.update_work_project_description import UpdateWorkProjectDescription

class TestUpdateWorkProjectDescription:
    
    def test_update_work_project_description_success(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectDescription(mock_repository)
        work_project_id = 1
        description = "Nova descrição detalhada do projeto"
        
        # Act
        use_case.update(work_project_id, description)
        
        # Assert
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"description": description}
        )
    
    def test_update_work_project_description_empty_string_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectDescription(mock_repository)
        work_project_id = 1
        description = ""
        
        # Act & Assert
        with pytest.raises(ValueError, match="Description cannot be empty"):
            use_case.update(work_project_id, description)
        
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_description_whitespace_only_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectDescription(mock_repository)
        work_project_id = 1
        description = "   "
        
        # Act & Assert
        with pytest.raises(ValueError, match="Description cannot be empty"):
            use_case.update(work_project_id, description)
        
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_description_none_raises_error(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectDescription(mock_repository)
        work_project_id = 1
        description = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Description cannot be empty"):
            use_case.update(work_project_id, description)
        
        mock_repository.update.assert_not_called()
    
    def test_update_work_project_description_strips_whitespace(self):
        # Arrange
        mock_repository = Mock()
        use_case = UpdateWorkProjectDescription(mock_repository)
        work_project_id = 1
        description = "  Descrição com Espaços  "
        
        # Act
        use_case.update(work_project_id, description)
        
        # Assert
        mock_repository.update.assert_called_once_with(
            work_project_id=work_project_id,
            update_params={"description": "Descrição com Espaços"}
        ) 