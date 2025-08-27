#pylint:disable=all
import pytest
from unittest.mock import Mock, AsyncMock
import json
from src.presentation.controllers.cache.bairro.set.set_bairro_by_name_cached_controller import SetBairroByNameCachedController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_set_cached_value import ISetCachedValue

class TestSetBairroByNameCachedController:
    
    @pytest.fixture
    def mock_set_cached_value(self):
        """Fixture to create a mock set cached value use case"""
        mock_use_case = Mock(spec=ISetCachedValue)
        mock_use_case.set = AsyncMock()
        return mock_use_case
    
    @pytest.fixture
    def controller(self, mock_set_cached_value):
        """Fixture to create a SetBairroByNameCachedController instance"""
        return SetBairroByNameCachedController(mock_set_cached_value)
    
    @pytest.mark.asyncio
    async def test_handle_success(self, controller, mock_set_cached_value):
        """Test successful handle operation"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = {
            "id": 1,
            "name": "Centro",
            "created_at": "2024-01-15"
        }
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['message'] == 'Bairro set successfully'
        assert result.body['content']['name'] == bairro_name
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_different_bairro_name(self, controller, mock_set_cached_value):
        """Test handle operation with different bairro name"""
        # Arrange
        bairro_name = "Vila Nova"
        bairro_data = {
            "id": 2,
            "name": "Vila Nova",
            "created_at": "2024-03-20"
        }
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == bairro_name
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_special_characters(self, controller, mock_set_cached_value):
        """Test handle operation with special characters in bairro name"""
        # Arrange
        bairro_name = "São João do Sul"
        bairro_data = {
            "id": 3,
            "name": "São João do Sul",
            "created_at": "2024-06-10"
        }
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == bairro_name
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_empty_bairro_name(self, controller, mock_set_cached_value):
        """Test handle operation with empty bairro name"""
        # Arrange
        bairro_name = ""
        bairro_data = {
            "id": 4,
            "name": "",
            "created_at": "2024-12-01"
        }
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == ""
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_long_bairro_name(self, controller, mock_set_cached_value):
        """Test handle operation with long bairro name"""
        # Arrange
        bairro_name = "Bairro com nome muito longo para testar o comportamento"
        bairro_data = {
            "id": 5,
            "name": bairro_name,
            "created_at": "2024-08-15"
        }
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == bairro_name
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_numeric_bairro_name(self, controller, mock_set_cached_value):
        """Test handle operation with numeric bairro name"""
        # Arrange
        bairro_name = "12345"
        bairro_data = {
            "id": 6,
            "name": "12345",
            "created_at": "2024-02-29"
        }
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == "12345"
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_complex_body_data(self, controller, mock_set_cached_value):
        """Test handle operation with complex body data"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = {
            "id": 1,
            "name": "Centro",
            "created_at": "2024-01-15",
            "population": 15000,
            "area": 2.5,
            "coordinates": {
                "lat": -28.2356,
                "lng": -48.6689
            },
            "features": ["shopping", "hospital", "school"]
        }
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == bairro_name
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_empty_body(self, controller, mock_set_cached_value):
        """Test handle operation with empty body"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = {}
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == bairro_name
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_none_body(self, controller, mock_set_cached_value):
        """Test handle operation with None body"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = None
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == bairro_name
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value="None")
    
    @pytest.mark.asyncio
    async def test_handle_with_use_case_exception(self, controller, mock_set_cached_value):
        """Test handle operation when use case raises an exception"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = {"id": 1, "name": "Centro"}
        mock_set_cached_value.set.side_effect = Exception("Cache error")
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Cache error"):
            await controller.handle(http_request)
        
        mock_set_cached_value.set.assert_called_once_with(key=bairro_name, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_missing_path_params(self, controller, mock_set_cached_value):
        """Test handle operation with missing path parameters"""
        # Arrange
        bairro_data = {"id": 1, "name": "Centro"}
        http_request = HttpRequest(
            path_params={},  # Missing name
            body=bairro_data
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] is None
        mock_set_cached_value.set.assert_called_once_with(key=None, value=json.dumps(bairro_data))
    
    @pytest.mark.asyncio
    async def test_handle_with_none_path_params(self, controller, mock_set_cached_value):
        """Test handle operation with None path parameters"""
        # Arrange
        bairro_data = {"id": 1, "name": "Centro"}
        http_request = HttpRequest(
            path_params=None,
            body=bairro_data
        )
        
        # Act & Assert
        with pytest.raises(AttributeError):
            await controller.handle(http_request)
    
    @pytest.mark.asyncio
    async def test_handle_with_connection_timeout(self, controller, mock_set_cached_value):
        """Test handle operation with connection timeout"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = {"id": 1, "name": "Centro"}
        mock_set_cached_value.set.side_effect = TimeoutError("Connection timeout")
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act & Assert
        with pytest.raises(TimeoutError, match="Connection timeout"):
            await controller.handle(http_request)
    
    @pytest.mark.asyncio
    async def test_handle_with_network_error(self, controller, mock_set_cached_value):
        """Test handle operation with network error"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = {"id": 1, "name": "Centro"}
        mock_set_cached_value.set.side_effect = ConnectionError("Network error")
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act & Assert
        with pytest.raises(ConnectionError, match="Network error"):
            await controller.handle(http_request)
    
    @pytest.mark.asyncio
    async def test_handle_with_redis_error(self, controller, mock_set_cached_value):
        """Test handle operation with Redis error"""
        # Arrange
        bairro_name = "Centro"
        bairro_data = {"id": 1, "name": "Centro"}
        mock_set_cached_value.set.side_effect = Exception("Redis connection failed")
        
        http_request = HttpRequest(
            path_params={'name': bairro_name},
            body=bairro_data
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Redis connection failed"):
            await controller.handle(http_request)
    
    def test_init_with_set_cached_value(self, mock_set_cached_value):
        """Test initialization with set cached value use case"""
        # Act
        controller = SetBairroByNameCachedController(mock_set_cached_value)
        
        # Assert
        assert controller.set_cached_value == mock_set_cached_value 