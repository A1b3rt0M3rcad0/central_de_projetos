#pylint:disable=all
import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import Request as FastAPIRequest
from src.main.adapters.generic_cache_aside_adapter import simple_cache_aside_adapter
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class TestCacheAsideAdapter:
    
    @pytest.fixture
    def mock_fastapi_request(self):
        """Fixture to create a mock FastAPI request"""
        mock_request = Mock(spec=FastAPIRequest)
        mock_request.headers = {"content-type": "application/json"}
        mock_request.query_params = {}
        mock_request.path_params = {"bairro_name": "Centro"}
        mock_request.url = "http://localhost:8000/bairro/Centro"
        return mock_request
    
    @pytest.fixture
    def mock_cache_get_controller(self):
        """Fixture to create a mock cache get controller (async)"""
        return AsyncMock()
    
    @pytest.fixture
    def mock_db_controller(self):
        """Fixture to create a mock database controller (sync)"""
        return Mock()
    
    @pytest.fixture
    def mock_cache_set_controller(self):
        """Fixture to create a mock cache set controller (async)"""
        return AsyncMock()
    
    @pytest.mark.asyncio
    async def test_cache_hit_success(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test successful cache hit - data found in cache"""
        # Arrange
        cache_response = HttpResponse(
            status_code=200,
            body={
                'messsage': 'Bairro Founded',
                'content': {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
            }
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Act
        result = await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        assert result == cache_response
        mock_cache_get_controller.assert_called_once()
        mock_db_controller.assert_not_called()
        mock_cache_set_controller.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_cache_miss_db_hit_success(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test cache miss but database hit - data found in database and cached"""
        # Arrange
        # Cache miss - returns None or empty content
        cache_response = HttpResponse(
            status_code=200,
            body={'content': None}
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Database hit
        db_response = HttpResponse(
            status_code=200,
            body={
                'messsage': 'Bairro Founded',
                'content': {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
            }
        )
        mock_db_controller.return_value = db_response
        
        # Cache set success
        mock_cache_set_controller.return_value = HttpResponse(status_code=200, body={'message': 'Cached'})
        
        # Act
        result = await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        assert result == db_response
        mock_cache_get_controller.assert_called_once()
        mock_db_controller.assert_called_once()
        mock_cache_set_controller.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_cache_exception_db_hit_success(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test cache exception but database hit - data found in database and cached"""
        # Arrange
        # Cache throws exception
        mock_cache_get_controller.side_effect = Exception("Cache error")
        
        # Database hit
        db_response = HttpResponse(
            status_code=200,
            body={
                'messsage': 'Bairro Founded',
                'content': {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
            }
        )
        mock_db_controller.return_value = db_response
        
        # Cache set success
        mock_cache_set_controller.return_value = HttpResponse(status_code=200, body={'message': 'Cached'})
        
        # Act
        result = await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        assert result == db_response
        mock_cache_get_controller.assert_called_once()
        mock_db_controller.assert_called_once()
        mock_cache_set_controller.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_cache_miss_db_hit_cache_set_failure(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test cache miss, database hit, but cache set fails - should still return db result"""
        # Arrange
        # Cache miss
        cache_response = HttpResponse(
            status_code=200,
            body={'content': None}
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Database hit
        db_response = HttpResponse(
            status_code=200,
            body={
                'messsage': 'Bairro Founded',
                'content': {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
            }
        )
        mock_db_controller.return_value = db_response
        
        # Cache set fails
        mock_cache_set_controller.side_effect = Exception("Cache set error")
        
        # Act
        result = await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        assert result == db_response
        mock_cache_get_controller.assert_called_once()
        mock_db_controller.assert_called_once()
        mock_cache_set_controller.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_cache_miss_db_miss(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test cache miss and database miss - should return db response (which will be error)"""
        # Arrange
        # Cache miss
        cache_response = HttpResponse(
            status_code=200,
            body={'content': None}
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Database miss - returns error response
        db_response = HttpResponse(
            status_code=404,
            body={'error': 'Bairro not found'}
        )
        mock_db_controller.return_value = db_response
        
        # Act
        result = await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        assert result == db_response
        mock_cache_get_controller.assert_called_once()
        mock_db_controller.assert_called_once()
        mock_cache_set_controller.assert_not_called()  # Should not cache error responses
    
    @pytest.mark.asyncio
    async def test_cache_miss_db_exception(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test cache miss and database exception - should propagate the exception"""
        # Arrange
        # Cache miss
        cache_response = HttpResponse(
            status_code=200,
            body={'content': None}
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Database throws exception
        mock_db_controller.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await simple_cache_aside_adapter(
                framework_request=mock_fastapi_request,
                cache_get_controller=mock_cache_get_controller,
                db_controller=mock_db_controller,
                cache_set_controller=mock_cache_set_controller,
                cache_key='bairro_name'
            )
        
        mock_cache_get_controller.assert_called_once()
        mock_db_controller.assert_called_once()
        mock_cache_set_controller.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_cache_hit_with_empty_content(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test cache hit but with empty content - should fallback to database"""
        # Arrange
        # Cache hit but empty content
        cache_response = HttpResponse(
            status_code=200,
            body={'content': {}}  # Empty content
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Database hit
        db_response = HttpResponse(
            status_code=200,
            body={
                'messsage': 'Bairro Founded',
                'content': {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
            }
        )
        mock_db_controller.return_value = db_response
        
        # Act
        result = await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        assert result == db_response
        mock_cache_get_controller.assert_called_once()
        mock_db_controller.assert_called_once()
        mock_cache_set_controller.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_cache_hit_with_no_content_key(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test cache hit but without content key - should fallback to database"""
        # Arrange
        # Cache hit but no content key
        cache_response = HttpResponse(
            status_code=200,
            body={'message': 'Success'}  # No content key
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Database hit
        db_response = HttpResponse(
            status_code=200,
            body={
                'messsage': 'Bairro Founded',
                'content': {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
            }
        )
        mock_db_controller.return_value = db_response
        
        # Act
        result = await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        assert result == db_response
        mock_cache_get_controller.assert_called_once()
        mock_db_controller.assert_called_once()
        mock_cache_set_controller.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_http_request_conversion(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test that FastAPI request is correctly converted to HttpRequest"""
        # Arrange
        cache_response = HttpResponse(
            status_code=200,
            body={
                'messsage': 'Bairro Founded',
                'content': {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
            }
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Act
        await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        mock_cache_get_controller.assert_called_once()
        called_request = mock_cache_get_controller.call_args[0][0]
        assert isinstance(called_request, HttpRequest)
        assert called_request.headers == {"content-type": "application/json"}
        assert called_request.path_params == {"bairro_name": "Centro"}
        assert called_request.url == "http://localhost:8000/bairro/Centro"
    
    @pytest.mark.asyncio
    async def test_sync_db_controller_handling(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test that sync database controller is handled correctly"""
        # Arrange
        # Cache miss
        cache_response = HttpResponse(
            status_code=200,
            body={'content': None}
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Database hit with sync controller
        db_response = HttpResponse(
            status_code=200,
            body={
                'messsage': 'Bairro Founded',
                'content': {'id': 1, 'name': 'Centro', 'created_at': '15/01/2024'}
            }
        )
        mock_db_controller.return_value = db_response
        
        # Cache set success
        mock_cache_set_controller.return_value = HttpResponse(status_code=200, body={'message': 'Cached'})
        
        # Act
        result = await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        assert result == db_response
        mock_db_controller.assert_called_once()
        # Verify that the sync controller was called (the adapter should handle both sync and async)
        assert mock_db_controller.call_count == 1

    @pytest.mark.asyncio
    async def test_access_token_not_cached(self, mock_fastapi_request, mock_cache_get_controller, mock_db_controller, mock_cache_set_controller):
        """Test that access_token is not stored in cache"""
        # Arrange
        # Cache miss
        cache_response = HttpResponse(
            status_code=200,
            body={'content': None}
        )
        mock_cache_get_controller.return_value = cache_response
        
        # Database hit with access_token in response
        db_response = HttpResponse(
            status_code=200,
            body={
                'messsage': 'Bairro Founded',
                'content': {
                    'id': 1, 
                    'name': 'Centro', 
                    'created_at': '15/01/2024',
                    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'  # Token que não deve ser cacheado
                }
            }
        )
        mock_db_controller.return_value = db_response
        
        # Cache set success
        mock_cache_set_controller.return_value = HttpResponse(status_code=200, body={'message': 'Cached'})
        
        # Act
        result = await simple_cache_aside_adapter(
            framework_request=mock_fastapi_request,
            cache_get_controller=mock_cache_get_controller,
            db_controller=mock_db_controller,
            cache_set_controller=mock_cache_set_controller,
            cache_key='bairro_name'
        )
        
        # Assert
        assert result == db_response
        mock_cache_get_controller.assert_called_once()
        mock_db_controller.assert_called_once()
        mock_cache_set_controller.assert_called_once()
        
        # Verify that the cache_set_controller was called with data WITHOUT access_token
        cache_set_call = mock_cache_set_controller.call_args[0][0]
        assert isinstance(cache_set_call, HttpRequest)
        assert 'access_token' not in cache_set_call.body
        assert cache_set_call.body == {
            'id': 1, 
            'name': 'Centro', 
            'created_at': '15/01/2024'
        } 