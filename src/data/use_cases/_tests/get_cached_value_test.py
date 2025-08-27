#pylint:disable=all
import pytest
from unittest.mock import Mock, AsyncMock
from src.data.use_cases.get_cached_value import GetCachedValue
from src.data.interface.i_cache_repository import ICacheRepository

class TestGetCachedValue:
    
    @pytest.fixture
    def mock_cache_repository(self):
        """Fixture to create a mock cache repository"""
        mock_repo = Mock(spec=ICacheRepository)
        mock_repo.get = AsyncMock()
        return mock_repo
    
    @pytest.fixture
    def get_cached_value(self, mock_cache_repository):
        """Fixture to create a GetCachedValue instance"""
        return GetCachedValue(mock_cache_repository)
    
    @pytest.mark.asyncio
    async def test_get_success(self, get_cached_value, mock_cache_repository):
        """Test successful get operation"""
        # Arrange
        key = "test_key"
        expected_value = "test_value"
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_key(self, get_cached_value, mock_cache_repository):
        """Test get operation with nonexistent key"""
        # Arrange
        key = "nonexistent_key"
        mock_cache_repository.get.return_value = None
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result is None
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_with_empty_key(self, get_cached_value, mock_cache_repository):
        """Test get operation with empty key"""
        # Arrange
        key = ""
        expected_value = "some_value"
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_with_special_characters(self, get_cached_value, mock_cache_repository):
        """Test get operation with special characters in key"""
        # Arrange
        key = "test_key_with_special_chars_!@#$%^&*()"
        expected_value = "test_value_with_special_chars_!@#$%^&*()"
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_with_long_key(self, get_cached_value, mock_cache_repository):
        """Test get operation with long key"""
        # Arrange
        key = "a" * 1000  # 1000 character key
        expected_value = "long_value"
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_with_numeric_key(self, get_cached_value, mock_cache_repository):
        """Test get operation with numeric key"""
        # Arrange
        key = "12345"
        expected_value = "67890"
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_with_unicode_key(self, get_cached_value, mock_cache_repository):
        """Test get operation with unicode key"""
        # Arrange
        key = "test_key_áéíóú_ñ_ç"
        expected_value = "test_value_áéíóú_ñ_ç"
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_with_whitespace_key(self, get_cached_value, mock_cache_repository):
        """Test get operation with whitespace in key"""
        # Arrange
        key = "  test_key_with_spaces  "
        expected_value = "  test_value_with_spaces  "
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_with_newlines_key(self, get_cached_value, mock_cache_repository):
        """Test get operation with newlines in key"""
        # Arrange
        key = "test_key\nwith\nnewlines"
        expected_value = "test_value\nwith\nnewlines"
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_empty_string_value(self, get_cached_value, mock_cache_repository):
        """Test get operation returning empty string"""
        # Arrange
        key = "test_key"
        expected_value = ""
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_large_value(self, get_cached_value, mock_cache_repository):
        """Test get operation with large value"""
        # Arrange
        key = "test_key"
        expected_value = "x" * 10000  # 10KB value
        mock_cache_repository.get.return_value = expected_value
        
        # Act
        result = await get_cached_value.get(key)
        
        # Assert
        assert result == expected_value
        assert len(result) == 10000
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_multiple_calls(self, get_cached_value, mock_cache_repository):
        """Test multiple get operations"""
        # Arrange
        operations = [
            ("key1", "value1"),
            ("key2", "value2"),
            ("key3", None)
        ]
        
        # Configure mock to return different values for different keys
        def mock_get_side_effect(key):
            for k, v in operations:
                if k == key:
                    return v
            return None
        
        mock_cache_repository.get.side_effect = mock_get_side_effect
        
        # Act
        results = []
        for key, _ in operations:
            result = await get_cached_value.get(key)
            results.append(result)
        
        # Assert
        assert results == ["value1", "value2", None]
        assert mock_cache_repository.get.call_count == 3
        expected_calls = [
            (("key1",),),
            (("key2",),),
            (("key3",),)
        ]
        mock_cache_repository.get.assert_has_calls(expected_calls)
    
    @pytest.mark.asyncio
    async def test_get_with_repository_exception(self, get_cached_value, mock_cache_repository):
        """Test get operation when repository raises an exception"""
        # Arrange
        key = "test_key"
        mock_cache_repository.get.side_effect = Exception("Redis connection error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Redis connection error"):
            await get_cached_value.get(key)
        
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_with_connection_timeout(self, get_cached_value, mock_cache_repository):
        """Test get operation with connection timeout"""
        # Arrange
        key = "test_key"
        mock_cache_repository.get.side_effect = TimeoutError("Connection timeout")
        
        # Act & Assert
        with pytest.raises(TimeoutError, match="Connection timeout"):
            await get_cached_value.get(key)
        
        mock_cache_repository.get.assert_called_once_with(key)
    
    @pytest.mark.asyncio
    async def test_get_with_network_error(self, get_cached_value, mock_cache_repository):
        """Test get operation with network error"""
        # Arrange
        key = "test_key"
        mock_cache_repository.get.side_effect = ConnectionError("Network error")
        
        # Act & Assert
        with pytest.raises(ConnectionError, match="Network error"):
            await get_cached_value.get(key)
        
        mock_cache_repository.get.assert_called_once_with(key)
    
    def test_init_with_cache_repository(self, mock_cache_repository):
        """Test initialization with cache repository"""
        # Act
        get_cached_value = GetCachedValue(mock_cache_repository)
        
        # Assert
        assert get_cached_value.cache_repository == mock_cache_repository 