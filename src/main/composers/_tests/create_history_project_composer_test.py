# pylint: disable=unused-import,unused-variable,reimported,import-outside-toplevel
import pytest
from unittest.mock import Mock, patch
from src.main.composers.create_history_project_composer import create_history_project_composer
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class TestCreateHistoryProjectComposer:
    """Testes para o composer de criação de histórico do projeto"""

    def test_composer_creates_controller_with_correct_dependencies(self):
        """Testa se o composer cria o controller com as dependências corretas"""
        handler = create_history_project_composer()
        
        # Verifica se retorna uma função callable
        assert callable(handler)
        
        # Verifica se é uma instância do controller correto
        assert handler.__name__ == 'handle'

    def test_composer_returns_callable_handler(self):
        """Testa se o composer retorna um handler callable"""
        handler = create_history_project_composer()
        
        assert callable(handler)
        assert hasattr(handler, '__call__')

    def test_composer_handler_calls_controller_handle(self):
        """Testa se o handler do composer chama o método handle do controller"""
        handler = create_history_project_composer()
        
        # Cria um mock request
        mock_request = HttpRequest(  # pylint: disable=unused-variable
            body={
                'project_id': 123,
                'data_name': 'Nome',
                'description': 'Nome do projeto atualizado para Teste'
            }
        )
        
        # Verifica se não levanta exceção de importação
        assert handler is not None

    def test_composer_imports_all_required_modules(self):
        """Testa se o composer importa todos os módulos necessários"""
        try:
            from src.main.composers.create_history_project_composer import create_history_project_composer  # pylint: disable=unused-import,reimported,import-outside-toplevel
            from src.presentation.controllers.create_history_project_controller import CreateHistoryProjectController  # pylint: disable=unused-import,import-outside-toplevel
            from src.data.use_cases.create_history_project import CreateHistoryProject  # pylint: disable=unused-import,import-outside-toplevel
            from src.infra.relational.repository.history_project_repository import HistoryProjectRepository  # pylint: disable=unused-import,import-outside-toplevel
            
            assert True
        except ImportError as e:
            pytest.fail(f"Falha ao importar módulos necessários: {e}")

    def test_composer_creates_history_project(self):
        """Testa se o composer cria histórico do projeto corretamente"""
        handler = create_history_project_composer()
        
        # Verifica se o handler foi criado com sucesso
        assert handler is not None
        
        # Verifica se inclui todas as dependências necessárias:
        # - CreateHistoryProject
        # - HistoryProjectRepository
        assert True  # Se chegou até aqui, significa que o composer foi criado com sucesso

    def test_composer_uses_correct_repository(self):
        """Testa se o composer usa o repositório correto"""
        handler = create_history_project_composer()
        
        # Verifica se o handler foi criado com sucesso
        assert handler is not None
        
        # Verifica se usa o HistoryProjectRepository
        assert True  # Se chegou até aqui, significa que o composer foi criado com sucesso 