#pylint:disable=W0143,W0613
import pytest
from unittest.mock import Mock, patch
from src.main.composers.create_work_project_with_fiscal_document_composer import create_work_project_with_fiscal_document_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class TestCreateWorkProjectWithFiscalDocumentComposer:
    
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.DBConnectionHandler')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.StringConnection')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.WorkProjectRepository')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.InsertWorkProject')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.RavenDBConnectionHandler')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.RavenDataConnection')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.ProjectDocumentFiscalRepository')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.SaveFiscalDocument')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.CreateWorkProjectWithFiscalDocumentController')
    def test_composer_creates_controller_with_correct_dependencies(
        self, 
        mock_controller_class, 
        mock_save_fiscal_document_class,
        mock_fiscal_repository_class,
        mock_raven_data_connection_class,
        mock_raven_db_handler_class,
        mock_insert_work_project_class,
        mock_work_project_repository_class,
        mock_string_connection_class,
        mock_db_handler_class
    ):
        """Testa se o composer cria o controller com as dependências corretas"""
        
        # Arrange
        mock_db_handler = Mock()
        mock_string_connection = Mock()
        mock_work_project_repository = Mock()
        mock_insert_work_project = Mock()
        mock_raven_db_handler = Mock()
        mock_raven_data_connection = Mock()
        mock_fiscal_repository = Mock()
        mock_save_fiscal_document = Mock()
        mock_controller = Mock()
        
        # Configurar os mocks para retornar as instâncias esperadas
        mock_db_handler_class.return_value = mock_db_handler
        mock_string_connection_class.return_value = mock_string_connection
        mock_work_project_repository_class.return_value = mock_work_project_repository
        mock_insert_work_project_class.return_value = mock_insert_work_project
        mock_raven_db_handler_class.return_value = mock_raven_db_handler
        mock_raven_data_connection_class.return_value = mock_raven_data_connection
        mock_fiscal_repository_class.return_value = mock_fiscal_repository
        mock_save_fiscal_document_class.return_value = mock_save_fiscal_document
        mock_controller_class.return_value = mock_controller
        
        # Act
        handler = create_work_project_with_fiscal_document_composer()
        
        # Assert
        # Verificar se as classes foram instanciadas corretamente
        mock_db_handler_class.assert_called_once_with(connection=mock_string_connection)
        mock_work_project_repository_class.assert_called_once_with(mock_db_handler)
        mock_insert_work_project_class.assert_called_once_with(mock_work_project_repository)
        
        mock_raven_db_handler_class.assert_called_once_with(data_connection=mock_raven_data_connection)
        mock_fiscal_repository_class.assert_called_once_with(mock_raven_db_handler)
        mock_save_fiscal_document_class.assert_called_once_with(mock_fiscal_repository)
        
        # Verificar se o controller foi criado com os casos de uso corretos
        mock_controller_class.assert_called_once_with(
            insert_work_project_case=mock_insert_work_project,
            save_fiscal_document_case=mock_save_fiscal_document
        )
        
        # Verificar se o handler retornado é o método handle do controller
        assert handler == mock_controller.handle
    
    def test_composer_returns_callable_handler(self):
        """Testa se o composer retorna um handler callable"""
        
        # Act
        handler = create_work_project_with_fiscal_document_composer()
        
        # Assert
        assert callable(handler)
    
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.DBConnectionHandler')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.StringConnection')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.WorkProjectRepository')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.InsertWorkProject')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.RavenDBConnectionHandler')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.RavenDataConnection')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.ProjectDocumentFiscalRepository')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.SaveFiscalDocument')
    @patch('src.main.composers.create_work_project_with_fiscal_document_composer.CreateWorkProjectWithFiscalDocumentController')
    def test_composer_handler_calls_controller_handle(
        self,
        mock_controller_class,
        mock_save_fiscal_document_class,
        mock_fiscal_repository_class,
        mock_raven_data_connection_class,
        mock_raven_db_handler_class,
        mock_insert_work_project_class,
        mock_work_project_repository_class,
        mock_string_connection_class,
        mock_db_handler_class
    ):
        """Testa se o handler retornado pelo composer chama o método handle do controller"""
        
        # Arrange
        mock_controller = Mock()
        mock_controller_class.return_value = mock_controller
        
        # Configurar o mock do controller para retornar uma resposta
        expected_response = HttpResponse(status_code=200, body={'message': 'success'})
        mock_controller.handle.return_value = expected_response
        
        # Act
        handler = create_work_project_with_fiscal_document_composer()
        
        # Simular uma requisição
        test_request = HttpRequest(body={
            'project_id': 1,
            'fiscal_id': 2,
            'title': 'Test',
            'description': 'Test description'
        })
        
        result = handler(test_request)
        
        # Assert
        mock_controller.handle.assert_called_once_with(test_request)
        assert result == expected_response
    
    def test_composer_imports_all_required_modules(self):
        """Testa se o composer importa todos os módulos necessários"""
        
        # Este teste verifica se não há erros de importação
        try:
            handler = create_work_project_with_fiscal_document_composer()
            assert callable(handler)
        except ImportError as e:
            pytest.fail(f"Erro de importação no composer: {e}")
        except Exception as e:
            pytest.fail(f"Erro inesperado no composer: {e}") 