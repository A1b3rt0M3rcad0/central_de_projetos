#pylint:disable=all
import pytest
from unittest.mock import Mock, patch
from src.main.composers.get_fiscal_summary_composer import get_fiscal_summary_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class TestGetFiscalSummaryComposer:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.mock_db_connection_handler = Mock()
        self.mock_fiscal_repository = Mock()
        self.mock_project_fiscal_repository = Mock()
        self.mock_work_project_repository = Mock()
        self.mock_get_fiscal_summary = Mock()
        self.mock_controller = Mock()
    
    @patch('src.main.composers.get_fiscal_summary_composer.db_connection_handler_factory')
    @patch('src.main.composers.get_fiscal_summary_composer.FiscalRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.ProjectFiscalRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.WorkProjectRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.GetFiscalSummary')
    @patch('src.main.composers.get_fiscal_summary_composer.GetFiscalSummaryController')
    def test_get_fiscal_summary_composer_returns_callable(
        self,
        mock_controller_class,
        mock_use_case_class,
        mock_work_project_repo_class,
        mock_project_fiscal_repo_class,
        mock_fiscal_repo_class,
        mock_db_factory
    ):
        """Testa se o composer retorna uma função callable"""
        # Arrange
        mock_db_factory.return_value = self.mock_db_connection_handler
        mock_fiscal_repo_class.return_value = self.mock_fiscal_repository
        mock_project_fiscal_repo_class.return_value = self.mock_project_fiscal_repository
        mock_work_project_repo_class.return_value = self.mock_work_project_repository
        mock_use_case_class.return_value = self.mock_get_fiscal_summary
        mock_controller_class.return_value = self.mock_controller
        
        # Act
        result = get_fiscal_summary_composer()
        
        # Assert
        assert callable(result)
        assert result == self.mock_controller.handle
    
    @patch('src.main.composers.get_fiscal_summary_composer.db_connection_handler_factory')
    @patch('src.main.composers.get_fiscal_summary_composer.FiscalRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.ProjectFiscalRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.WorkProjectRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.GetFiscalSummary')
    @patch('src.main.composers.get_fiscal_summary_composer.GetFiscalSummaryController')
    def test_get_fiscal_summary_composer_dependencies(
        self,
        mock_controller_class,
        mock_use_case_class,
        mock_work_project_repo_class,
        mock_project_fiscal_repo_class,
        mock_fiscal_repo_class,
        mock_db_factory
    ):
        """Testa se as dependências são criadas corretamente"""
        # Arrange
        mock_db_factory.return_value = self.mock_db_connection_handler
        mock_fiscal_repo_class.return_value = self.mock_fiscal_repository
        mock_project_fiscal_repo_class.return_value = self.mock_project_fiscal_repository
        mock_work_project_repo_class.return_value = self.mock_work_project_repository
        mock_use_case_class.return_value = self.mock_get_fiscal_summary
        mock_controller_class.return_value = self.mock_controller
        
        # Act
        get_fiscal_summary_composer()
        
        # Assert
        # Verificar se db_connection_handler_factory foi chamado (3 vezes, uma para cada repository)
        assert mock_db_factory.call_count == 3
        
        # Verificar se os repositories foram criados com o db_connection_handler correto
        mock_fiscal_repo_class.assert_called_once_with(
            db_connection_handler=self.mock_db_connection_handler
        )
        mock_project_fiscal_repo_class.assert_called_once_with(
            db_connection_handler=self.mock_db_connection_handler
        )
        mock_work_project_repo_class.assert_called_once_with(
            db_connection_handler=self.mock_db_connection_handler
        )
        
        # Verificar se o use case foi criado com os repositories corretos
        mock_use_case_class.assert_called_once_with(
            fiscal_repository=self.mock_fiscal_repository,
            project_fiscal_repository=self.mock_project_fiscal_repository,
            work_project_repository=self.mock_work_project_repository
        )
        
        # Verificar se o controller foi criado com o use case correto
        mock_controller_class.assert_called_once_with(
            get_fiscal_summary=self.mock_get_fiscal_summary
        )
    
    @patch('src.main.composers.get_fiscal_summary_composer.db_connection_handler_factory')
    @patch('src.main.composers.get_fiscal_summary_composer.FiscalRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.ProjectFiscalRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.WorkProjectRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.GetFiscalSummary')
    @patch('src.main.composers.get_fiscal_summary_composer.GetFiscalSummaryController')
    def test_get_fiscal_summary_composer_integration(
        self,
        mock_controller_class,
        mock_use_case_class,
        mock_work_project_repo_class,
        mock_project_fiscal_repo_class,
        mock_fiscal_repo_class,
        mock_db_factory
    ):
        """Testa a integração do composer com uma requisição real"""
        # Arrange
        mock_db_factory.return_value = self.mock_db_connection_handler
        mock_fiscal_repo_class.return_value = self.mock_fiscal_repository
        mock_project_fiscal_repo_class.return_value = self.mock_project_fiscal_repository
        mock_work_project_repo_class.return_value = self.mock_work_project_repository
        mock_use_case_class.return_value = self.mock_get_fiscal_summary
        mock_controller_class.return_value = self.mock_controller
        
        # Mock da resposta do controller
        expected_response = HttpResponse(
            status_code=200,
            body={
                'message': 'Fiscal Summary Retrieved Successfully',
                'fiscal_id': 1,
                'content': {
                    'fiscal': {'id': 1, 'name': 'Test'},
                    'total_projetos_vinculados': 2,
                    'total_fiscalizacoes': 3,
                    'fiscalizacoes_no_periodo': 2,
                    'last_activity_at': '01/01/2024 10:00:00',
                    'fiscalizacoes_por_projeto': [],
                    'ultimas_fiscalizacoes': [],
                    'documentos_enviados': 0
                }
            }
        )
        self.mock_controller.handle.return_value = expected_response
        
        # Act
        handler = get_fiscal_summary_composer()
        http_request = HttpRequest(
            body={'fiscal_id': 1},
            query_params={'limit': '5'}
        )
        result = handler(http_request)
        
        # Assert
        assert result == expected_response
        self.mock_controller.handle.assert_called_once_with(http_request)
    
    @patch('src.main.composers.get_fiscal_summary_composer.db_connection_handler_factory')
    @patch('src.main.composers.get_fiscal_summary_composer.FiscalRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.ProjectFiscalRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.WorkProjectRepository')
    @patch('src.main.composers.get_fiscal_summary_composer.GetFiscalSummary')
    @patch('src.main.composers.get_fiscal_summary_composer.GetFiscalSummaryController')
    def test_get_fiscal_summary_composer_error_handling(
        self,
        mock_controller_class,
        mock_use_case_class,
        mock_work_project_repo_class,
        mock_project_fiscal_repo_class,
        mock_fiscal_repo_class,
        mock_db_factory
    ):
        """Testa o tratamento de erro do composer"""
        # Arrange
        mock_db_factory.return_value = self.mock_db_connection_handler
        mock_fiscal_repo_class.return_value = self.mock_fiscal_repository
        mock_project_fiscal_repo_class.return_value = self.mock_project_fiscal_repository
        mock_work_project_repo_class.return_value = self.mock_work_project_repository
        mock_use_case_class.return_value = self.mock_get_fiscal_summary
        mock_controller_class.return_value = self.mock_controller
        
        # Mock de erro do controller
        self.mock_controller.handle.side_effect = Exception("Test error")
        
        # Act
        handler = get_fiscal_summary_composer()
        http_request = HttpRequest(
            body={'fiscal_id': 1},
            query_params={}
        )
        
        # Assert
        with pytest.raises(Exception, match="Test error"):
            handler(http_request) 