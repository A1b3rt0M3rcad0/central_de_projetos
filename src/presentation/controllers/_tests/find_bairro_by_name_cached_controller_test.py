#pylint:disable=all
import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from src.presentation.controllers.cache.bairro.get.find_bairro_by_name_cached_controller import FindBairroByNameCachedController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_get_cached_value import IGetCachedValue
import json

class TestFindBairroByNameCachedController:
    
    @pytest.fixture
    def mock_get_cached_value(self):
        """Fixture to create a mock get cached value use case"""
        mock_use_case = Mock(spec=IGetCachedValue)
        mock_use_case.get = AsyncMock()
        return mock_use_case
    
    @pytest.fixture
    def controller(self, mock_get_cached_value):
        """Fixture to create a FindBairroByNameCachedController instance"""
        return FindBairroByNameCachedController(mock_get_cached_value)
    
    @pytest.mark.asyncio
    async def test_handle_success(self, controller, mock_get_cached_value):
        """Test successful handle operation"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
        cached_data = json.dumps(bairro_data)
        
        mock_get_cached_value.get.return_value = cached_data
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['messsage'] == 'Bairro Founded'
        assert result.body['content'] == bairro_data
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_different_bairro_name(self, controller, mock_get_cached_value):
        """Test handle operation with different bairro name"""
        # Arrange
        bairro_name = "Vila Nova"
        bairro_data = {'id': 2, 'name': 'Vila Nova', 'created_at': '20/03/2024'}
        cached_data = json.dumps(bairro_data)
        
        mock_get_cached_value.get.return_value = cached_data
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content'] == bairro_data
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_special_characters(self, controller, mock_get_cached_value):
        """Test handle operation with special characters in bairro name"""
        # Arrange
        bairro_name = "São João do Sul"
        bairro_data = {'id': 3, 'name': 'São João do Sul', 'created_at': '10/06/2024'}
        cached_data = json.dumps(bairro_data)
        
        mock_get_cached_value.get.return_value = cached_data
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content'] == bairro_data
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_empty_bairro_name(self, controller, mock_get_cached_value):
        """Test handle operation with empty bairro name"""
        # Arrange
        bairro_name = ""
        bairro_data = {'id': 4, 'name': '', 'created_at': '01/12/2024'}
        cached_data = json.dumps(bairro_data)
        
        mock_get_cached_value.get.return_value = cached_data
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content'] == bairro_data
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_long_bairro_name(self, controller, mock_get_cached_value):
        """Test handle operation with long bairro name"""
        # Arrange
        bairro_name = "Bairro com nome muito longo para testar o comportamento"
        bairro_data = {'id': 5, 'name': bairro_name, 'created_at': '15/08/2024'}
        cached_data = json.dumps(bairro_data)
        
        mock_get_cached_value.get.return_value = cached_data
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content'] == bairro_data
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_numeric_bairro_name(self, controller, mock_get_cached_value):
        """Test handle operation with numeric bairro name"""
        # Arrange
        bairro_name = "12345"
        bairro_data = {'id': 6, 'name': '12345', 'created_at': '29/02/2024'}
        cached_data = json.dumps(bairro_data)
        
        mock_get_cached_value.get.return_value = cached_data
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content'] == bairro_data
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_none_result(self, controller, mock_get_cached_value):
        """Test handle operation when cache returns None"""
        # Arrange
        bairro_name = "Centro"
        mock_get_cached_value.get.return_value = None
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content'] is None
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_invalid_json(self, controller, mock_get_cached_value):
        """Test handle operation with invalid JSON in cache"""
        # Arrange
        bairro_name = "Centro"
        invalid_json = "invalid json string"
        
        mock_get_cached_value.get.return_value = invalid_json
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content'] == invalid_json
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_dict_result(self, controller, mock_get_cached_value):
        """Test handle operation when cache returns a dict directly"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
        
        mock_get_cached_value.get.return_value = bairro_data
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content'] == bairro_data
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_use_case_exception(self, controller, mock_get_cached_value):
        """Test handle operation when use case raises an exception"""
        # Arrange
        bairro_name = "Centro"
        mock_get_cached_value.get.side_effect = Exception("Cache error")
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Cache error"):
            await controller.handle(http_request)
        
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_missing_path_params(self, controller, mock_get_cached_value):
        """Test handle operation with missing path parameters"""
        # Arrange
        http_request = HttpRequest(
            path_params={}  # Missing bairro_name
        )
        
        # Act & Assert
        with pytest.raises(KeyError):
            await controller.handle(http_request)
    
    @pytest.mark.asyncio
    async def test_handle_with_none_path_params(self, controller, mock_get_cached_value):
        """Test handle operation with None path parameters"""
        # Arrange
        http_request = HttpRequest(
            path_params=None
        )
        
        # Act & Assert
        with pytest.raises(TypeError):
            await controller.handle(http_request)
    
    @pytest.mark.asyncio
    async def test_handle_with_connection_timeout(self, controller, mock_get_cached_value):
        """Test handle operation with connection timeout"""
        # Arrange
        bairro_name = "Centro"
        mock_get_cached_value.get.side_effect = TimeoutError("Connection timeout")
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act & Assert
        with pytest.raises(TimeoutError, match="Connection timeout"):
            await controller.handle(http_request)
    
    @pytest.mark.asyncio
    async def test_handle_with_network_error(self, controller, mock_get_cached_value):
        """Test handle operation with network error"""
        # Arrange
        bairro_name = "Centro"
        mock_get_cached_value.get.side_effect = ConnectionError("Network error")
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act & Assert
        with pytest.raises(ConnectionError, match="Network error"):
            await controller.handle(http_request)
    
    def test_init_with_get_cached_value(self, mock_get_cached_value):
        """Test initialization with get cached value use case"""
        # Act
        controller = FindBairroByNameCachedController(mock_get_cached_value)
        
        # Assert
        assert controller.get_cached_value == mock_get_cached_value 