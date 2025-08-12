#pylint:disable=all
import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from src.presentation.controllers.get_fiscal_summary_controller import GetFiscalSummaryController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class TestGetFiscalSummaryController:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.mock_get_fiscal_summary = Mock()
        self.controller = GetFiscalSummaryController(self.mock_get_fiscal_summary)
    
    def test_handle_success(self):
        """Testa o sucesso do controller"""
        # Arrange
        fiscal_id = 1
        start_date = "2024-01-01T00:00:00"
        end_date = "2024-12-31T23:59:59"
        limit = 5
        
        mock_result = {
            'fiscal': {
                'id': fiscal_id,
                'name': 'Fiscal Teste',
                'email': 'fiscal@teste.com',
                'phone': '11999999999'
            },
            'total_projetos_vinculados': 2,
            'total_fiscalizacoes': 3,
            'fiscalizacoes_no_periodo': 2,
            'last_activity_at': '01/01/2024 10:00:00',
            'fiscalizacoes_por_projeto': [
                {'project_id': 1, 'project_name': 'Projeto 1', 'count': 3}
            ],
            'ultimas_fiscalizacoes': [
                {'id': 1, 'title': 'WP 1', 'project_id': 1, 'project_name': 'Projeto 1', 'created_at': '01/01/2024 10:00:00'}
            ],
            'documentos_enviados': 6
        }
        
        self.mock_get_fiscal_summary.get_summary.return_value = mock_result
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            query_params={
                'start_date': start_date,
                'end_date': end_date,
                'limit': str(limit)
            }
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Fiscal Summary Retrieved Successfully'
        assert result.body['fiscal_id'] == fiscal_id
        assert result.body['start_date'] == start_date
        assert result.body['end_date'] == end_date
        assert result.body['content'] == mock_result
        
        # Verificar se o use case foi chamado corretamente
        self.mock_get_fiscal_summary.get_summary.assert_called_once()
        call_args = self.mock_get_fiscal_summary.get_summary.call_args
        assert call_args[1]['fiscal_id'] == fiscal_id
        assert call_args[1]['limit'] == limit
        assert call_args[1]['start_date'].isoformat() == start_date
        assert call_args[1]['end_date'].isoformat() == end_date
    
    def test_handle_without_date_filter(self):
        """Testa o controller sem filtro de data"""
        # Arrange
        fiscal_id = 1
        
        mock_result = {
            'fiscal': {
                'id': fiscal_id,
                'name': 'Fiscal Teste',
                'email': 'fiscal@teste.com',
                'phone': '11999999999'
            },
            'total_projetos_vinculados': 0,
            'total_fiscalizacoes': 2,
            'fiscalizacoes_no_periodo': 2,
            'last_activity_at': '01/01/2024 10:00:00',
            'fiscalizacoes_por_projeto': [],
            'ultimas_fiscalizacoes': [],
            'documentos_enviados': 0
        }
        
        self.mock_get_fiscal_summary.get_summary.return_value = mock_result
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            query_params={}
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['start_date'] is None
        assert result.body['end_date'] is None
        assert result.body['content'] == mock_result
        
        # Verificar se o use case foi chamado com valores padrão
        call_args = self.mock_get_fiscal_summary.get_summary.call_args
        assert call_args[1]['start_date'] is None
        assert call_args[1]['end_date'] is None
        assert call_args[1]['limit'] == 5  # valor padrão
    
    def test_handle_with_custom_limit(self):
        """Testa o controller com limite personalizado"""
        # Arrange
        fiscal_id = 1
        limit = 10
        
        mock_result = {
            'fiscal': {
                'id': fiscal_id,
                'name': 'Fiscal Teste',
                'email': 'fiscal@teste.com',
                'phone': '11999999999'
            },
            'total_projetos_vinculados': 1,
            'total_fiscalizacoes': 5,
            'fiscalizacoes_no_periodo': 5,
            'last_activity_at': '01/01/2024 10:00:00',
            'fiscalizacoes_por_projeto': [],
            'ultimas_fiscalizacoes': [],
            'documentos_enviados': 0
        }
        
        self.mock_get_fiscal_summary.get_summary.return_value = mock_result
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            query_params={'limit': str(limit)}
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        
        # Verificar se o use case foi chamado com o limite correto
        call_args = self.mock_get_fiscal_summary.get_summary.call_args
        assert call_args[1]['limit'] == limit
    
    def test_handle_missing_fiscal_id(self):
        """Testa o controller sem fiscal_id"""
        # Arrange
        http_request = HttpRequest(
            body={},
            query_params={}
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 400
        assert result.body['error'] == 'fiscal_id is required'
        
        # Verificar se o use case não foi chamado
        self.mock_get_fiscal_summary.get_summary.assert_not_called()
    
    def test_handle_invalid_start_date(self):
        """Testa o controller com data de início inválida"""
        # Arrange
        fiscal_id = 1
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            query_params={'start_date': 'invalid-date'}
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 400
        assert 'start_date must be in ISO format' in result.body['error']
        
        # Verificar se o use case não foi chamado
        self.mock_get_fiscal_summary.get_summary.assert_not_called()
    
    def test_handle_invalid_end_date(self):
        """Testa o controller com data de fim inválida"""
        # Arrange
        fiscal_id = 1
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            query_params={'end_date': 'invalid-date'}
        )
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 400
        assert 'end_date must be in ISO format' in result.body['error']
        
        # Verificar se o use case não foi chamado
        self.mock_get_fiscal_summary.get_summary.assert_not_called()
    
    def test_handle_invalid_limit(self):
        """Testa o controller com limite inválido"""
        # Arrange
        fiscal_id = 1
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            query_params={'limit': 'invalid'}
        )
        
        mock_result = {
            'fiscal': {
                'id': fiscal_id,
                'name': 'Fiscal Teste',
                'email': 'fiscal@teste.com',
                'phone': '11999999999'
            },
            'total_projetos_vinculados': 0,
            'total_fiscalizacoes': 0,
            'fiscalizacoes_no_periodo': 0,
            'last_activity_at': None,
            'fiscalizacoes_por_projeto': [],
            'ultimas_fiscalizacoes': [],
            'documentos_enviados': 0
        }
        
        self.mock_get_fiscal_summary.get_summary.return_value = mock_result
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        
        # Verificar se o use case foi chamado com limite padrão
        call_args = self.mock_get_fiscal_summary.get_summary.call_args
        assert call_args[1]['limit'] == 5  # valor padrão quando inválido
    
    def test_handle_negative_limit(self):
        """Testa o controller com limite negativo"""
        # Arrange
        fiscal_id = 1
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            query_params={'limit': '-1'}
        )
        
        mock_result = {
            'fiscal': {
                'id': fiscal_id,
                'name': 'Fiscal Teste',
                'email': 'fiscal@teste.com',
                'phone': '11999999999'
            },
            'total_projetos_vinculados': 0,
            'total_fiscalizacoes': 0,
            'fiscalizacoes_no_periodo': 0,
            'last_activity_at': None,
            'fiscalizacoes_por_projeto': [],
            'ultimas_fiscalizacoes': [],
            'documentos_enviados': 0
        }
        
        self.mock_get_fiscal_summary.get_summary.return_value = mock_result
        
        # Act
        result = self.controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        
        # Verificar se o use case foi chamado com limite padrão
        call_args = self.mock_get_fiscal_summary.get_summary.call_args
        assert call_args[1]['limit'] == 5  # valor padrão quando negativo
    
    def test_handle_exception(self):
        """Testa o controller quando o use case lança exceção"""
        # Arrange
        fiscal_id = 1
        
        self.mock_get_fiscal_summary.get_summary.side_effect = Exception("Test error")
        
        http_request = HttpRequest(
            body={'fiscal_id': fiscal_id},
            query_params={}
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Test error"):
            self.controller.handle(http_request) 