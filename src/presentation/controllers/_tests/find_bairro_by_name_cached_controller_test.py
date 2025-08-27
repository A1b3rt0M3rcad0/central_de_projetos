#pylint:disable=all
import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from src.presentation.controllers.cache.bairro.get.find_bairro_by_name_cached_controller import FindBairroByNameCachedController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_get_cached_value import IGetCachedValue

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
        mock_bairro = Mock()
        mock_bairro.bairro = 1
        mock_bairro.name = "Centro"
        mock_bairro.created_at = datetime(2024, 1, 15)
        
        mock_get_cached_value.get.return_value = mock_bairro
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert isinstance(result, HttpResponse)
        assert result.status_code == 200
        assert result.body['messsage'] == 'Bairro Founded'
        assert result.body['content']['id'] == 1
        assert result.body['content']['name'] == "Centro"
        assert result.body['content']['created_at'] == "15/01/2024"
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_different_bairro_name(self, controller, mock_get_cached_value):
        """Test handle operation with different bairro name"""
        # Arrange
        bairro_name = "Vila Nova"
        mock_bairro = Mock()
        mock_bairro.bairro = 2
        mock_bairro.name = "Vila Nova"
        mock_bairro.created_at = datetime(2024, 3, 20)
        
        mock_get_cached_value.get.return_value = mock_bairro
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['id'] == 2
        assert result.body['content']['name'] == "Vila Nova"
        assert result.body['content']['created_at'] == "20/03/2024"
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_special_characters(self, controller, mock_get_cached_value):
        """Test handle operation with special characters in bairro name"""
        # Arrange
        bairro_name = "São João do Sul"
        mock_bairro = Mock()
        mock_bairro.bairro = 3
        mock_bairro.name = "São João do Sul"
        mock_bairro.created_at = datetime(2024, 6, 10)
        
        mock_get_cached_value.get.return_value = mock_bairro
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == "São João do Sul"
        assert result.body['content']['created_at'] == "10/06/2024"
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_empty_bairro_name(self, controller, mock_get_cached_value):
        """Test handle operation with empty bairro name"""
        # Arrange
        bairro_name = ""
        mock_bairro = Mock()
        mock_bairro.bairro = 4
        mock_bairro.name = ""
        mock_bairro.created_at = datetime(2024, 12, 1)
        
        mock_get_cached_value.get.return_value = mock_bairro
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == ""
        assert result.body['content']['created_at'] == "01/12/2024"
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_long_bairro_name(self, controller, mock_get_cached_value):
        """Test handle operation with long bairro name"""
        # Arrange
        bairro_name = "Bairro com nome muito longo para testar o comportamento"
        mock_bairro = Mock()
        mock_bairro.bairro = 5
        mock_bairro.name = bairro_name
        mock_bairro.created_at = datetime(2024, 8, 15)
        
        mock_get_cached_value.get.return_value = mock_bairro
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == bairro_name
        assert result.body['content']['created_at'] == "15/08/2024"
        mock_get_cached_value.get.assert_called_once_with(key=bairro_name)
    
    @pytest.mark.asyncio
    async def test_handle_with_numeric_bairro_name(self, controller, mock_get_cached_value):
        """Test handle operation with numeric bairro name"""
        # Arrange
        bairro_name = "12345"
        mock_bairro = Mock()
        mock_bairro.bairro = 6
        mock_bairro.name = "12345"
        mock_bairro.created_at = datetime(2024, 2, 29)
        
        mock_get_cached_value.get.return_value = mock_bairro
        
        http_request = HttpRequest(
            path_params={'bairro_name': bairro_name}
        )
        
        # Act
        result = await controller.handle(http_request)
        
        # Assert
        assert result.status_code == 200
        assert result.body['content']['name'] == "12345"
        assert result.body['content']['created_at'] == "29/02/2024"
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