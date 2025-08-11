#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.main.composers.get_work_projects_by_fiscal_mobile_composer import get_work_projects_by_fiscal_mobile_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class TestGetWorkProjectsByFiscalMobileComposer:

    def test_composer_returns_callable(self):
        """Testa se o composer retorna uma função callable"""
        # Act
        handler = get_work_projects_by_fiscal_mobile_composer()
        
        # Assert
        assert callable(handler)
        assert hasattr(handler, '__call__')

    def test_composer_handler_signature(self):
        """Testa se o handler tem a assinatura correta"""
        # Act
        handler = get_work_projects_by_fiscal_mobile_composer()
        
        # Assert
        import inspect
        sig = inspect.signature(handler)
        assert len(sig.parameters) == 1
        assert 'http_request' in sig.parameters

    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobileController')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobile')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.FindProjectFiscal')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.WorkProjectRepository')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.ProjectFiscalRepository')
    def test_composer_handler_returns_http_response(self, mock_project_fiscal_repo_class, mock_work_project_repo_class, mock_find_project_fiscal_class, mock_use_case_class, mock_controller_class):
        """Testa se o handler retorna HttpResponse"""
        # Arrange
        # Mock repositories
        mock_work_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project_fiscal = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_fiscal_class.return_value = mock_find_project_fiscal
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.return_value = HttpResponse(
            status_code=200,
            body={'message': 'Success'}
        )
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = get_work_projects_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={'fiscal_id': 1},
            path_params={
                'project_id': 2,
                'page': 1,
                'page_size': 10
            }
        )
        result = handler(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Success'

    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobileController')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobile')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.FindProjectFiscal')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.WorkProjectRepository')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.ProjectFiscalRepository')
    def test_composer_handler_with_valid_data(self, mock_project_fiscal_repo_class, mock_work_project_repo_class, mock_find_project_fiscal_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com dados válidos"""
        # Arrange
        # Mock repositories
        mock_work_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project_fiscal = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_fiscal_class.return_value = mock_find_project_fiscal
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.return_value = HttpResponse(
            status_code=200,
            body={
                'message': 'Work Projects Founded',
                'total': 1,
                'page': 1,
                'page_size': 10,
                'project_id': 2,
                'fiscal_id': 1,
                'content': []
            }
        )
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = get_work_projects_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={'fiscal_id': 1},
            path_params={
                'project_id': 2,
                'page': 1,
                'page_size': 10
            }
        )
        result = handler(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['message'] == 'Work Projects Founded'
        assert result.body['total'] == 1
        assert result.body['page'] == 1
        assert result.body['page_size'] == 10
        assert result.body['project_id'] == 2
        assert result.body['fiscal_id'] == 1

    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobileController')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobile')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.FindProjectFiscal')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.WorkProjectRepository')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.ProjectFiscalRepository')
    def test_composer_handler_with_error(self, mock_project_fiscal_repo_class, mock_work_project_repo_class, mock_find_project_fiscal_class, mock_use_case_class, mock_controller_class):
        """Testa o handler quando ocorre erro"""
        # Arrange
        # Mock repositories
        mock_work_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project_fiscal = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_fiscal_class.return_value = mock_find_project_fiscal
        
        # Mock controller para simular erro
        mock_controller = Mock()
        mock_controller.handle.side_effect = Exception("Test error")
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_work_projects_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={'fiscal_id': 1},
            path_params={
                'project_id': 2,
                'page': 1,
                'page_size': 10
            }
        )
        
        with pytest.raises(Exception) as exc_info:
            handler(http_request)
        
        assert "Test error" in str(exc_info.value)

    def test_composer_dependencies_injection(self):
        """Testa se as dependências são injetadas corretamente"""
        # Arrange
        with patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobile') as mock_use_case_class, \
             patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.FindProjectFiscal') as mock_find_project_fiscal_class, \
             patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.WorkProjectRepository') as mock_work_project_repo_class, \
             patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.ProjectFiscalRepository') as mock_project_fiscal_repo_class, \
             patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobileController') as mock_controller_class:
            
            # Mock instances
            mock_work_project_repo = Mock()
            mock_project_fiscal_repo = Mock()
            mock_use_case = Mock()
            mock_find_project_fiscal = Mock()
            mock_controller = Mock()
            
            # Setup mocks
            mock_work_project_repo_class.return_value = mock_work_project_repo
            mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
            mock_use_case_class.return_value = mock_use_case
            mock_find_project_fiscal_class.return_value = mock_find_project_fiscal
            mock_controller_class.return_value = mock_controller
            
            # Act
            handler = get_work_projects_by_fiscal_mobile_composer()
            
            # Assert
            # Verificar se os repositories foram instanciados
            mock_work_project_repo_class.assert_called_once()
            mock_project_fiscal_repo_class.assert_called_once()
            
            # Verificar se os use cases foram instanciados com os repositories corretos
            mock_use_case_class.assert_called_once_with(mock_work_project_repo)
            mock_find_project_fiscal_class.assert_called_once_with(mock_project_fiscal_repo)
            
            # Verificar se o controller foi instanciado com os use cases corretos
            mock_controller_class.assert_called_once_with(
                get_work_projects_by_fiscal_mobile_case=mock_use_case,
                find_project_fiscal_case=mock_find_project_fiscal
            )

    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobileController')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobile')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.FindProjectFiscal')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.WorkProjectRepository')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.ProjectFiscalRepository')
    def test_composer_handler_with_missing_fiscal_id(self, mock_project_fiscal_repo_class, mock_work_project_repo_class, mock_find_project_fiscal_class, mock_use_case_class, mock_controller_class):
        """Testa o handler quando fiscal_id está faltando"""
        # Arrange
        # Mock repositories
        mock_work_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project_fiscal = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_fiscal_class.return_value = mock_find_project_fiscal
        
        # Mock controller para simular erro de validação
        mock_controller = Mock()
        mock_controller.handle.return_value = HttpResponse(
            status_code=400,
            body={'error': 'fiscal_id is required'}
        )
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = get_work_projects_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={},  # fiscal_id faltando
            path_params={
                'project_id': 2,
                'page': 1,
                'page_size': 10
            }
        )
        result = handler(http_request)
        
        # Assert
        assert result.status_code == 400
        assert result.body['error'] == 'fiscal_id is required'

    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobileController')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobile')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.FindProjectFiscal')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.WorkProjectRepository')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.ProjectFiscalRepository')
    def test_composer_handler_with_missing_project_id(self, mock_project_fiscal_repo_class, mock_work_project_repo_class, mock_find_project_fiscal_class, mock_use_case_class, mock_controller_class):
        """Testa o handler quando project_id está faltando"""
        # Arrange
        # Mock repositories
        mock_work_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project_fiscal = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_fiscal_class.return_value = mock_find_project_fiscal
        
        # Mock controller para simular erro de validação
        mock_controller = Mock()
        mock_controller.handle.return_value = HttpResponse(
            status_code=400,
            body={'error': 'project_id is required'}
        )
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = get_work_projects_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={'fiscal_id': 1},
            path_params={
                'page': 1,
                'page_size': 10
                # project_id faltando
            }
        )
        result = handler(http_request)
        
        # Assert
        assert result.status_code == 400
        assert result.body['error'] == 'project_id is required'

    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobileController')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.GetWorkProjectsByFiscalMobile')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.FindProjectFiscal')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.WorkProjectRepository')
    @patch('src.main.composers.get_work_projects_by_fiscal_mobile_composer.ProjectFiscalRepository')
    def test_composer_handler_with_fiscal_not_authorized(self, mock_project_fiscal_repo_class, mock_work_project_repo_class, mock_find_project_fiscal_class, mock_use_case_class, mock_controller_class):
        """Testa o handler quando fiscal não está autorizado"""
        # Arrange
        # Mock repositories
        mock_work_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project_fiscal = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_fiscal_class.return_value = mock_find_project_fiscal
        
        # Mock controller para simular erro de autorização
        from src.errors.use_cases.fiscal_not_authorized_error import FiscalNotAuthorizedError
        mock_controller = Mock()
        mock_controller.handle.side_effect = FiscalNotAuthorizedError(
            title="FiscalNotAuthorizedError",
            message="Fiscal 1 não está autorizado a acessar work projects do projeto 2"
        )
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_work_projects_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={'fiscal_id': 1},
            path_params={
                'project_id': 2,
                'page': 1,
                'page_size': 10
            }
        )
        
        with pytest.raises(FiscalNotAuthorizedError) as exc_info:
            handler(http_request)
        
        assert "Fiscal 1 não está autorizado a acessar work projects do projeto 2" in str(exc_info.value) 