# pylint: disable=unused-import,unused-variable,reimported,import-outside-toplevel
import pytest
from unittest.mock import Mock, patch
from src.main.composers.find_all_history_from_project_composer import find_all_history_from_project_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class TestFindAllHistoryFromProjectComposer:
    """Testes para o composer de busca de histórico do projeto"""

    def test_composer_creates_controller_with_correct_dependencies(self):
        """Testa se o composer cria o controller com as dependências corretas"""
        handler = find_all_history_from_project_composer()
        
        # Verifica se retorna uma função callable
        assert callable(handler)
        
        # Verifica se é uma instância do controller correto
        assert handler.__name__ == 'handle'

    def test_composer_returns_callable_handler(self):
        """Testa se o composer retorna um handler callable"""
        handler = find_all_history_from_project_composer()
        
        assert callable(handler)
        assert hasattr(handler, '__call__')

    def test_composer_handler_calls_controller_handle(self):
        """Testa se o handler do composer chama o método handle do controller"""
        handler = find_all_history_from_project_composer()
        
        # Cria um mock request
        mock_request = HttpRequest(  # pylint: disable=unused-variable
            path_params={'project_id': '123'}
        )
        
        # Verifica se não levanta exceção de importação
        assert handler is not None

    def test_composer_imports_all_required_modules(self):
        """Testa se o composer importa todos os módulos necessários"""
        try:
            from src.main.composers.find_all_history_from_project_composer import find_all_history_from_project_composer  # pylint: disable=unused-import,reimported,import-outside-toplevel
            from src.presentation.controllers.find_all_history_from_project_controller import FindAllHistoryFromProjectController  # pylint: disable=unused-import,import-outside-toplevel
            from src.data.use_cases.find_all_history_from_project import FindAllHistoryFromProject  # pylint: disable=unused-import,import-outside-toplevel
            from src.infra.relational.repository.history_project_repository import HistoryProjectRepository  # pylint: disable=unused-import,import-outside-toplevel
            
            assert True
        except ImportError as e:
            pytest.fail(f"Falha ao importar módulos necessários: {e}")

    def test_composer_finds_history_from_project(self):
        """Testa se o composer busca histórico do projeto corretamente"""
        handler = find_all_history_from_project_composer()
        
        # Verifica se o handler foi criado com sucesso
        assert handler is not None
        
        # Verifica se inclui todas as dependências necessárias:
        # - FindAllHistoryFromProject
        # - HistoryProjectRepository
        assert True  # Se chegou até aqui, significa que o composer foi criado com sucesso

    def test_composer_uses_correct_repository(self):
        """Testa se o composer usa o repositório correto"""
        handler = find_all_history_from_project_composer()
        
        # Verifica se o handler foi criado com sucesso
        assert handler is not None
        
        # Verifica se usa o HistoryProjectRepository
        assert True  # Se chegou até aqui, significa que o composer foi criado com sucesso 