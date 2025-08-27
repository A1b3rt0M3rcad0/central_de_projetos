#pylint:disable=all
import pytest
from unittest.mock import Mock, AsyncMock
from src.data.use_cases.set_cached_value import SetCachedValue
from src.data.interface.i_cache_repository import ICacheRepository

class TestSetCachedValue:
    
    @pytest.fixture
    def mock_cache_repository(self):
        """Fixture to create a mock cache repository"""
        mock_repo = Mock(spec=ICacheRepository)
        mock_repo.set = AsyncMock()
        return mock_repo
    
    @pytest.fixture
    def set_cached_value(self, mock_cache_repository):
        """Fixture to create a SetCachedValue instance"""
        return SetCachedValue(mock_cache_repository)
    
    @pytest.mark.asyncio
    async def test_set_success(self, set_cached_value, mock_cache_repository):
        """Test successful set operation"""
        # Arrange
        key = "test_key"
        value = "test_value"
        
        # Act
        await set_cached_value.set(key, value)
        
        # Assert
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    @pytest.mark.asyncio
    async def test_set_with_empty_key(self, set_cached_value, mock_cache_repository):
        """Test set operation with empty key"""
        # Arrange
        key = ""
        value = "test_value"
        
        # Act
        await set_cached_value.set(key, value)
        
        # Assert
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    @pytest.mark.asyncio
    async def test_set_with_empty_value(self, set_cached_value, mock_cache_repository):
        """Test set operation with empty value"""
        # Arrange
        key = "test_key"
        value = ""
        
        # Act
        await set_cached_value.set(key, value)
        
        # Assert
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    @pytest.mark.asyncio
    async def test_set_with_special_characters(self, set_cached_value, mock_cache_repository):
        """Test set operation with special characters in key and value"""
        # Arrange
        key = "test_key_with_special_chars_!@#$%^&*()"
        value = "test_value_with_special_chars_!@#$%^&*()"
        
        # Act
        await set_cached_value.set(key, value)
        
        # Assert
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    @pytest.mark.asyncio
    async def test_set_with_long_strings(self, set_cached_value, mock_cache_repository):
        """Test set operation with long key and value"""
        # Arrange
        key = "a" * 1000  # 1000 character key
        value = "b" * 1000  # 1000 character value
        
        # Act
        await set_cached_value.set(key, value)
        
        # Assert
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    @pytest.mark.asyncio
    async def test_set_with_numeric_strings(self, set_cached_value, mock_cache_repository):
        """Test set operation with numeric strings"""
        # Arrange
        key = "12345"
        value = "67890"
        
        # Act
        await set_cached_value.set(key, value)
        
        # Assert
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    @pytest.mark.asyncio
    async def test_set_with_unicode_strings(self, set_cached_value, mock_cache_repository):
        """Test set operation with unicode strings"""
        # Arrange
        key = "test_key_áéíóú_ñ_ç"
        value = "test_value_áéíóú_ñ_ç"
        
        # Act
        await set_cached_value.set(key, value)
        
        # Assert
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    @pytest.mark.asyncio
    async def test_set_with_whitespace(self, set_cached_value, mock_cache_repository):
        """Test set operation with whitespace in key and value"""
        # Arrange
        key = "  test_key_with_spaces  "
        value = "  test_value_with_spaces  "
        
        # Act
        await set_cached_value.set(key, value)
        
        # Assert
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    @pytest.mark.asyncio
    async def test_set_with_newlines(self, set_cached_value, mock_cache_repository):
        """Test set operation with newlines in key and value"""
        # Arrange
        key = "test_key\nwith\nnewlines"
        value = "test_value\nwith\nnewlines"
        
        # Act
        await set_cached_value.set(key, value)
        
        # Assert
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    @pytest.mark.asyncio
    async def test_set_multiple_calls(self, set_cached_value, mock_cache_repository):
        """Test multiple set operations"""
        # Arrange
        operations = [
            ("key1", "value1"),
            ("key2", "value2"),
            ("key3", "value3")
        ]
        
        # Act
        for key, value in operations:
            await set_cached_value.set(key, value)
        
        # Assert
        assert mock_cache_repository.set.call_count == 3
        expected_calls = [
            (("key1", "value1"),),
            (("key2", "value2"),),
            (("key3", "value3"),)
        ]
        mock_cache_repository.set.assert_has_calls(expected_calls)
    
    @pytest.mark.asyncio
    async def test_set_with_repository_exception(self, set_cached_value, mock_cache_repository):
        """Test set operation when repository raises an exception"""
        # Arrange
        key = "test_key"
        value = "test_value"
        mock_cache_repository.set.side_effect = Exception("Redis connection error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Redis connection error"):
            await set_cached_value.set(key, value)
        
        mock_cache_repository.set.assert_called_once_with(key, value)
    
    def test_init_with_cache_repository(self, mock_cache_repository):
        """Test initialization with cache repository"""
        # Act
        set_cached_value = SetCachedValue(mock_cache_repository)
        
        # Assert
        assert set_cached_value.cache_repository == mock_cache_repository 