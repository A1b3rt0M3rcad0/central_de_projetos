import pytest
from src.main.composers.delete_work_project_composer import delete_work_project_composer
from src.presentation.http_types.http_request import HttpRequest
#pylint:disable=W0611
from src.presentation.http_types.http_response import HttpResponse
from src.errors.use_cases.delete_work_project_error import DeleteWorkProjectError

class TestDeleteWorkProjectComposerIntegration:
    
    def test_delete_work_project_composer_returns_callable(self):
        """Testa se o composer retorna uma função callable"""
        # Act
        controller = delete_work_project_composer()
        
        # Assert
        assert callable(controller)
        assert controller.__name__ == 'handle'
    
    def test_delete_work_project_composer_handles_invalid_work_project_id(self):
        """Testa se o composer lida corretamente com work project ID inválido"""
        # Arrange
        work_project_id = 999999  # ID que não existe
        http_request = HttpRequest(
            path_params={'work_project_id': work_project_id}
        )
        
        # Act & Assert
        controller = delete_work_project_composer()
        
        # Deve lançar uma exceção quando o work project não existe
        with pytest.raises(DeleteWorkProjectError):
            controller(http_request)
    
    def test_delete_work_project_composer_handles_missing_work_project_id(self):
        """Testa se o composer lida corretamente com work project ID ausente"""
        # Arrange
        http_request = HttpRequest(
            path_params={}  # Sem work_project_id
        )
        
        # Act
        controller = delete_work_project_composer()
        
        # Assert
        # Deve lançar uma exceção por falta do parâmetro
        with pytest.raises(Exception):
            controller(http_request)
    
    def test_delete_work_project_composer_handles_string_work_project_id(self):
        """Testa se o composer lida corretamente com work project ID como string"""
        # Arrange
        http_request = HttpRequest(
            path_params={'work_project_id': 'invalid_id'}
        )
        
        # Act
        controller = delete_work_project_composer()
        
        # Assert
        # Deve lançar uma exceção por tipo inválido
        with pytest.raises(Exception):
            controller(http_request) 