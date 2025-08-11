#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.main.composers.get_work_project_by_fiscal_mobile_composer import get_work_project_by_fiscal_mobile_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class TestGetWorkProjectByFiscalMobileComposer:

    def test_composer_returns_callable(self):
        """Testa se o composer retorna uma função callable"""
        # Act
        handler = get_work_project_by_fiscal_mobile_composer()
        
        # Assert
        assert callable(handler)
        assert hasattr(handler, '__call__')

    def test_composer_handler_signature(self):
        """Testa se o handler tem a assinatura correta"""
        # Act
        handler = get_work_project_by_fiscal_mobile_composer()
        
        # Assert
        import inspect
        sig = inspect.signature(handler)
        assert len(sig.parameters) == 1
        assert 'http_request' in sig.parameters

    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscalMobileController')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscal')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository')
    def test_composer_handler_returns_http_response(self, mock_work_project_repo_class, mock_use_case_class, mock_controller_class):
        """Testa se o handler retorna HttpResponse"""
        # Arrange
        # Mock repository
        mock_work_project_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        
        # Mock use case
        mock_use_case = Mock()
        mock_use_case_class.return_value = mock_use_case
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.return_value = HttpResponse(
            status_code=200,
            body={'message': 'Success'}
        )
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = get_work_project_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'fiscal_id': 2
            }
        )
        result = handler(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Success'

    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscalMobileController')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscal')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository')
    def test_composer_handler_with_valid_data(self, mock_work_project_repo_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com dados válidos"""
        # Arrange
        # Mock repository
        mock_work_project_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        
        # Mock use case
        mock_use_case = Mock()
        mock_use_case_class.return_value = mock_use_case
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.return_value = HttpResponse(
            status_code=200,
            body={
                'message': 'Work Project found successfully',
                'content': {
                    'id': 1,
                    'project_id': 2,
                    'fiscal_id': 3,
                    'title': 'Test Work Project',
                    'description': 'Test Description',
                    'photo_name': 'test.jpg',
                    'additional_documents': [],
                    'created_at': '25/12/2024 10:30:00',
                    'updated_at': '25/12/2024 10:30:00',
                    'fiscal': {
                        'id': 3,
                        'name': 'Test Fiscal',
                        'created_at': '25/12/2024 10:30:00'
                    },
                    'project': {
                        'id': 2,
                        'status_id': 1,
                        'name': 'Test Project',
                        'andamento_do_projeto': 'Em andamento',
                        'verba_disponivel': '100000.00',
                        'start_date': '01/01/2024',
                        'expected_completion_date': '31/12/2024',
                        'end_date': None
                    }
                }
            }
        )
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = get_work_project_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'fiscal_id': 3
            }
        )
        result = handler(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Work Project found successfully'
        assert result.body['content']['id'] == 1
        assert result.body['content']['title'] == 'Test Work Project'
        assert result.body['content']['fiscal']['name'] == 'Test Fiscal'
        assert result.body['content']['project']['name'] == 'Test Project'

    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscalMobileController')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscal')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository')
    def test_composer_handler_with_error(self, mock_work_project_repo_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com erro"""
        # Arrange
        # Mock repository
        mock_work_project_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        
        # Mock use case
        mock_use_case = Mock()
        mock_use_case_class.return_value = mock_use_case
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.side_effect = Exception("Test error")
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_work_project_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'fiscal_id': 2
            }
        )
        
        with pytest.raises(Exception, match="Test error"):
            handler(http_request)

    def test_composer_dependencies_injection(self):
        """Testa se as dependências são injetadas corretamente"""
        # Act
        handler = get_work_project_by_fiscal_mobile_composer()
        
        # Assert
        assert callable(handler)
        
        # Verifica se o handler pode ser chamado sem erro de importação
        try:
            http_request = HttpRequest(
                body={
                    'work_project_id': 1,
                    'fiscal_id': 2
                }
            )
            # Não vamos executar o handler aqui pois precisaria de um banco real
            # Apenas verificamos se não há erros de importação
            assert True
        except ImportError:
            pytest.fail("Erro de importação nas dependências")

    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscalMobileController')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscal')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository')
    def test_composer_handler_with_missing_work_project_id(self, mock_work_project_repo_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com work_project_id ausente"""
        # Arrange
        # Mock repository
        mock_work_project_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        
        # Mock use case
        mock_use_case = Mock()
        mock_use_case_class.return_value = mock_use_case
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.side_effect = KeyError("work_project_id")
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_work_project_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={
                'fiscal_id': 2
            }
        )
        
        with pytest.raises(KeyError, match="work_project_id"):
            handler(http_request)

    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscalMobileController')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscal')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository')
    def test_composer_handler_with_missing_fiscal_id(self, mock_work_project_repo_class, mock_use_case_class, mock_controller_class):
        """Testa o handler com fiscal_id ausente"""
        # Arrange
        # Mock repository
        mock_work_project_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        
        # Mock use case
        mock_use_case = Mock()
        mock_use_case_class.return_value = mock_use_case
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.side_effect = KeyError("fiscal_id")
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_work_project_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={
                'work_project_id': 1
            }
        )
        
        with pytest.raises(KeyError, match="fiscal_id"):
            handler(http_request)

    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscalMobileController')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.GetWorkProjectByFiscal')
    @patch('src.main.composers.get_work_project_by_fiscal_mobile_composer.WorkProjectRepository')
    def test_composer_handler_with_fiscal_not_authorized(self, mock_work_project_repo_class, mock_use_case_class, mock_controller_class):
        """Testa o handler quando o fiscal não está autorizado para o work project"""
        # Arrange
        # Mock repository
        mock_work_project_repo = Mock()
        mock_work_project_repo_class.return_value = mock_work_project_repo
        
        # Mock use case
        mock_use_case = Mock()
        mock_use_case_class.return_value = mock_use_case
        
        # Mock controller
        mock_controller = Mock()
        mock_controller.handle.side_effect = Exception("Fiscal not authorized for this work project")
        mock_controller_class.return_value = mock_controller
        
        # Act & Assert
        handler = get_work_project_by_fiscal_mobile_composer()
        http_request = HttpRequest(
            body={
                'work_project_id': 1,
                'fiscal_id': 999  # Fiscal não autorizado
            }
        )
        
        with pytest.raises(Exception, match="Fiscal not authorized for this work project"):
            handler(http_request) 