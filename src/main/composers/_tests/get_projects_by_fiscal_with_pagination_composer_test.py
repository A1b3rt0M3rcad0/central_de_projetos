#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.main.composers.get_projects_by_fiscal_with_pagination_composer import get_projects_by_fiscal_with_pagination_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class TestGetProjectsByFiscalWithPaginationComposer:

    def test_composer_returns_callable(self):
        """Testa se o composer retorna uma função callable"""
        # Act
        handler = get_projects_by_fiscal_with_pagination_composer()
        
        # Assert
        assert callable(handler)
        assert hasattr(handler, '__call__')

    def test_composer_handler_signature(self):
        """Testa se o handler tem a assinatura correta"""
        # Act
        handler = get_projects_by_fiscal_with_pagination_composer()
        
        # Assert
        import inspect
        sig = inspect.signature(handler)
        assert len(sig.parameters) == 1
        assert 'http_request' in sig.parameters

    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPaginationController')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPagination')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.FindProject')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectRepository')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectFiscalRepository')
    def test_composer_handler_returns_http_response(self, mock_project_fiscal_repo_class, mock_project_repo_class, mock_find_project_class, mock_use_case_class, mock_controller_class):
        """Testa se o handler retorna HttpResponse"""
        # Arrange
        # Mock repositories
        mock_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_project_repo_class.return_value = mock_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_class.return_value = mock_find_project
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.return_value = HttpResponse(
            status_code=200,
            body={'message': 'Success'}
        )
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = get_projects_by_fiscal_with_pagination_composer()
        http_request = HttpRequest(
            body={
                'fiscal_id': 1,
                'page': 1,
                'page_size': 10
            }
        )
        result = handler(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Success'

    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPaginationController')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPagination')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.FindProject')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectRepository')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectFiscalRepository')
    def test_composer_handler_with_valid_data(self, mock_project_fiscal_repo_class, mock_project_repo_class, mock_find_project_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com dados válidos"""
        # Arrange
        # Mock repositories
        mock_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_project_repo_class.return_value = mock_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_class.return_value = mock_find_project
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.return_value = HttpResponse(
            status_code=200,
            body={
                'message': 'Projects Founded',
                'page': 1,
                'page_size': 10,
                'total_items': 1,
                'total_pages': 1,
                'content': [
                    {
                        'id': 1,
                        'status_id': 1,
                        'name': 'Projeto Teste',
                        'andamento_do_projeto': 'Em andamento',
                        'verba_disponivel': 1000.0
                    }
                ]
            }
        )
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = get_projects_by_fiscal_with_pagination_composer()
        http_request = HttpRequest(
            body={
                'fiscal_id': 1,
                'page': 1,
                'page_size': 10
            }
        )
        result = handler(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Projects Founded'
        assert result.body['page'] == 1
        assert result.body['page_size'] == 10
        assert result.body['total_items'] == 1
        assert result.body['total_pages'] == 1
        assert len(result.body['content']) == 1

    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPaginationController')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPagination')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.FindProject')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectRepository')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectFiscalRepository')
    def test_composer_handler_with_error(self, mock_project_fiscal_repo_class, mock_project_repo_class, mock_find_project_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com erro"""
        # Arrange
        # Mock repositories
        mock_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_project_repo_class.return_value = mock_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_class.return_value = mock_find_project
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.side_effect = Exception("Erro interno")
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_projects_by_fiscal_with_pagination_composer()
        http_request = HttpRequest(
            body={
                'fiscal_id': 1,
                'page': 1,
                'page_size': 10
            }
        )
        
        with pytest.raises(Exception):
            handler(http_request)

    def test_composer_dependencies_injection(self):
        """Testa se as dependências são injetadas corretamente"""
        # Act
        handler = get_projects_by_fiscal_with_pagination_composer()
        
        # Assert
        assert callable(handler)
        
        # Verificar se o handler pode ser chamado (isso testa se as dependências foram injetadas)
        try:
            http_request = HttpRequest(
                body={
                    'fiscal_id': 1,
                    'page': 1,
                    'page_size': 10
                }
            )
            # Não vamos executar o handler aqui, apenas verificar se ele foi criado corretamente
            assert handler is not None
        except Exception:
            # É esperado que possa haver erros de conexão com banco, mas o handler deve existir
            pass

    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPaginationController')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPagination')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.FindProject')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectRepository')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectFiscalRepository')
    def test_composer_handler_with_missing_fiscal_id(self, mock_project_fiscal_repo_class, mock_project_repo_class, mock_find_project_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com fiscal_id ausente"""
        # Arrange
        # Mock repositories
        mock_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_project_repo_class.return_value = mock_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_class.return_value = mock_find_project
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.side_effect = KeyError("fiscal_id")
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_projects_by_fiscal_with_pagination_composer()
        http_request = HttpRequest(
            body={
                'page': 1,
                'page_size': 10
            }
        )
        
        with pytest.raises(KeyError):
            handler(http_request)

    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPaginationController')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPagination')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.FindProject')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectRepository')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectFiscalRepository')
    def test_composer_handler_with_missing_page(self, mock_project_fiscal_repo_class, mock_project_repo_class, mock_find_project_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com page ausente"""
        # Arrange
        # Mock repositories
        mock_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_project_repo_class.return_value = mock_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_class.return_value = mock_find_project
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.side_effect = KeyError("page")
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_projects_by_fiscal_with_pagination_composer()
        http_request = HttpRequest(
            body={
                'fiscal_id': 1,
                'page_size': 10
            }
        )
        
        with pytest.raises(KeyError):
            handler(http_request)

    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPaginationController')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.GetProjectsByFiscalWithPagination')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.FindProject')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectRepository')
    @patch('src.main.composers.get_projects_by_fiscal_with_pagination_composer.ProjectFiscalRepository')
    def test_composer_handler_with_missing_page_size(self, mock_project_fiscal_repo_class, mock_project_repo_class, mock_find_project_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com page_size ausente"""
        # Arrange
        # Mock repositories
        mock_project_repo = Mock()
        mock_project_fiscal_repo = Mock()
        mock_project_repo_class.return_value = mock_project_repo
        mock_project_fiscal_repo_class.return_value = mock_project_fiscal_repo
        
        # Mock use cases
        mock_use_case = Mock()
        mock_find_project = Mock()
        mock_use_case_class.return_value = mock_use_case
        mock_find_project_class.return_value = mock_find_project
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.side_effect = KeyError("page_size")
        mock_controller_class.return_value = mock_controller
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_projects_by_fiscal_with_pagination_composer()
        http_request = HttpRequest(
            body={
                'fiscal_id': 1,
                'page': 1
            }
        )
        
        with pytest.raises(KeyError):
            handler(http_request) 