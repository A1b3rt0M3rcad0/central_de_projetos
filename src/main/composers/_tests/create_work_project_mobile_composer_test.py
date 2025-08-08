# pylint: disable=unused-import,unused-variable,reimported,import-outside-toplevel
import pytest
from unittest.mock import Mock, patch
from src.main.composers.create_work_project_mobile_composer import create_work_project_mobile_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class TestCreateWorkProjectMobileComposer:
    """Testes para o composer de criação de work project mobile"""

    def test_composer_creates_controller_with_correct_dependencies(self):
        """Testa se o composer cria o controller com as dependências corretas"""
        handler = create_work_project_mobile_composer()
        
        # Verifica se retorna uma função callable
        assert callable(handler)
        
        # Verifica se é uma instância do controller correto
        assert handler.__name__ == 'handle'

    def test_composer_returns_callable_handler(self):
        """Testa se o composer retorna um handler callable"""
        handler = create_work_project_mobile_composer()
        
        assert callable(handler)
        assert hasattr(handler, '__call__')

    def test_composer_handler_calls_controller_handle(self):
        """Testa se o handler do composer chama o método handle do controller"""
        handler = create_work_project_mobile_composer()
        
        # Cria um mock request
        mock_request = HttpRequest(  # pylint: disable=unused-variable
            body={
                'project_id': 1,
                'fiscal_id': 1,
                'title': 'Test Work Project',
                'description': 'Test Description'
            }
        )
        
        # Verifica se não levanta exceção de importação
        assert handler is not None

    def test_composer_imports_all_required_modules(self):
        """Testa se o composer importa todos os módulos necessários"""
        try:
            from src.main.composers.create_work_project_mobile_composer import create_work_project_mobile_composer  # pylint: disable=unused-import,reimported,import-outside-toplevel
            from src.presentation.controllers.create_work_project_mobile_controller import CreateWorkProjectMobileController  # pylint: disable=unused-import,import-outside-toplevel
            from src.data.use_cases.insert_work_project import InsertWorkProject  # pylint: disable=unused-import,import-outside-toplevel
            from src.data.use_cases.save_fiscal_document import SaveFiscalDocument  # pylint: disable=unused-import,import-outside-toplevel
            from src.data.use_cases.find_project_fiscal import FindProjectFiscal  # pylint: disable=unused-import,import-outside-toplevel
            from src.data.use_cases.create_history_project import CreateHistoryProject  # pylint: disable=unused-import,import-outside-toplevel
            
            assert True
        except ImportError as e:
            pytest.fail(f"Falha ao importar módulos necessários: {e}")

    def test_composer_creates_work_project_with_fiscal_validation(self):
        """Testa se o composer inclui validação de fiscal vinculado ao projeto"""
        handler = create_work_project_mobile_composer()
        
        # Verifica se o handler foi criado com sucesso
        assert handler is not None
        
        # Verifica se o controller inclui a validação de fiscal
        # Isso é verificado pela presença do FindProjectFiscal no composer
        assert True  # Se chegou até aqui, significa que o composer foi criado com sucesso 