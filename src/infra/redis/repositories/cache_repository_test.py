#pylint:disable=all
import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from src.infra.redis.config.connection.redis_url_connection import RedisUrlConnection
from src.infra.redis.repositories.cache_repository import CacheRepository
from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler

class TestCacheRepository:
    
    def setup_method(self):
        """Setup method to clear environment variables before each test"""
        # Clear Redis environment variables
        env_vars = ['REDIS_NAMESPACE', 'REDIS_TTL']
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]
    
    @pytest.fixture
    def mock_redis_connection_handler(self):
        """Fixture to create a mock RedisConnectionHandler"""
        mock_handler = Mock(spec=RedisConnectionHandler)
        mock_handler.__aenter__ = AsyncMock()
        mock_handler.__aexit__ = AsyncMock()
        return mock_handler
    
    @pytest.fixture
    def cache_repository(self, mock_redis_connection_handler):
        """Fixture to create a CacheRepository instance with mocked dependencies"""
        return CacheRepository(mock_redis_connection_handler)
    
    def test_init_with_default_values(self, mock_redis_connection_handler):
        """Test initialization with default values"""
        # Arrange - Clear environment to test default values
        with patch.dict(os.environ, {}, clear=True):
            with patch('src.infra.redis.repositories.cache_repository.load_dotenv'):
                # Act
                repository = CacheRepository(mock_redis_connection_handler)
                
                # Assert
                assert repository.NAMESPACE == "DEFAULT:"
                assert repository.TTL == 360
                assert repository._CacheRepository__redis_connection_handler == mock_redis_connection_handler
    
    def test_init_with_custom_values(self, mock_redis_connection_handler):
        """Test initialization with custom environment variables"""
        # Arrange
        test_env = {
            'REDIS_NAMESPACE': 'test_app',
            'REDIS_TTL': '7200'
        }
        
        # Act
        with patch.dict(os.environ, test_env):
            repository = CacheRepository(mock_redis_connection_handler)
        
        # Assert
        assert repository.NAMESPACE == "TEST_APP:"
        assert repository.TTL == 7200
    
    def test_ns_key_method(self, cache_repository):
        """Test the _ns_key method"""
        # Arrange
        key = "test_key"
        
        # Act
        result = cache_repository._ns_key(key)
        
        # Assert
        assert result == "IMBITUBA:test_key"  # Using actual environment value
    
    @pytest.mark.asyncio
    async def test_set_success(self, cache_repository, mock_redis_connection_handler):
        """Test successful set operation"""
        # Arrange
        key = "test_key"
        mapping = {"field1": "value1", "field2": "value2"}
        mock_redis = AsyncMock()
        mock_redis.hset = AsyncMock()
        mock_redis.expire = AsyncMock()
        mock_redis_connection_handler.__aenter__.return_value = mock_redis
        
        # Act
        result = await cache_repository.set(key, mapping)
        
        # Assert
        assert result is True
        mock_redis.hset.assert_called_once_with("IMBITUBA:test_key", mapping=mapping)
        mock_redis.expire.assert_called_once_with("IMBITUBA:test_key", 360)
    
    @pytest.mark.asyncio
    async def test_set_with_exception(self, cache_repository, mock_redis_connection_handler):
        """Test set operation with exception"""
        # Arrange
        key = "test_key"
        mapping = {"field1": "value1"}
        mock_redis = AsyncMock()
        mock_redis.hset = AsyncMock(side_effect=Exception("Redis error"))
        mock_redis_connection_handler.__aenter__.return_value = mock_redis
        mock_redis_connection_handler.__aexit__.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception, match="Redis error"):
            await cache_repository.set(key, mapping)
    
    @pytest.mark.asyncio
    async def test_get_success(self, cache_repository, mock_redis_connection_handler):
        """Test successful get operation"""
        # Arrange
        key = "test_key"
        expected_data = {"field1": "value1", "field2": "value2"}
        mock_redis = AsyncMock()
        mock_redis.hgetall = AsyncMock(return_value=expected_data)
        mock_redis_connection_handler.__aenter__.return_value = mock_redis
        
        # Act
        result = await cache_repository.get(key)
        
        # Assert
        assert result == expected_data
        mock_redis.hgetall.assert_called_once_with("IMBITUBA:test_key")
    
    @pytest.mark.asyncio
    async def test_get_with_exception(self, cache_repository, mock_redis_connection_handler):
        """Test get operation with exception"""
        # Arrange
        key = "test_key"
        mock_redis = AsyncMock()
        mock_redis.hgetall = AsyncMock(side_effect=Exception("Redis error"))
        mock_redis_connection_handler.__aenter__.return_value = mock_redis
        mock_redis_connection_handler.__aexit__.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception, match="Redis error"):
            await cache_repository.get(key)
    
    @pytest.mark.asyncio
    async def test_delete_success(self, cache_repository, mock_redis_connection_handler):
        """Test successful delete operation"""
        # Arrange
        key = "test_key"
        mock_redis = AsyncMock()
        mock_redis.delete = AsyncMock()
        mock_redis_connection_handler.__aenter__.return_value = mock_redis
        
        # Act
        result = await cache_repository.delete(key)
        
        # Assert
        assert result is True
        mock_redis.delete.assert_called_once_with("IMBITUBA:test_key")
    
    @pytest.mark.asyncio
    async def test_delete_with_exception(self, cache_repository, mock_redis_connection_handler):
        """Test delete operation with exception"""
        # Arrange
        key = "test_key"
        mock_redis = AsyncMock()
        mock_redis.delete = AsyncMock(side_effect=Exception("Redis error"))
        mock_redis_connection_handler.__aenter__.return_value = mock_redis
        mock_redis_connection_handler.__aexit__.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception, match="Redis error"):
            await cache_repository.delete(key)
    
    @pytest.mark.asyncio
    async def test_set_with_empty_mapping(self, cache_repository, mock_redis_connection_handler):
        """Test set operation with empty mapping"""
        # Arrange
        key = "test_key"
        mapping = {}
        mock_redis = AsyncMock()
        mock_redis.hset = AsyncMock()
        mock_redis.expire = AsyncMock()
        mock_redis_connection_handler.__aenter__.return_value = mock_redis
        
        # Act
        result = await cache_repository.set(key, mapping)
        
        # Assert
        assert result is True
        mock_redis.hset.assert_called_once_with("IMBITUBA:test_key", mapping=mapping)
        mock_redis.expire.assert_called_once_with("IMBITUBA:test_key", 360)
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_key(self, cache_repository, mock_redis_connection_handler):
        """Test get operation with nonexistent key"""
        # Arrange
        key = "nonexistent_key"
        mock_redis = AsyncMock()
        mock_redis.hgetall = AsyncMock(return_value={})
        mock_redis_connection_handler.__aenter__.return_value = mock_redis
        
        # Act
        result = await cache_repository.get(key)
        
        # Assert
        assert result == {}
    
    def test_namespace_with_special_characters(self, mock_redis_connection_handler):
        """Test namespace handling with special characters"""
        # Arrange
        test_env = {'REDIS_NAMESPACE': 'my-app_123'}
        
        # Act
        with patch.dict(os.environ, test_env):
            repository = CacheRepository(mock_redis_connection_handler)
        
        # Assert
        assert repository.NAMESPACE == "MY-APP_123:"
    
    def test_ttl_with_invalid_value(self, mock_redis_connection_handler):
        """Test TTL handling with invalid value"""
        # Arrange
        test_env = {'REDIS_TTL': 'invalid'}
        
        # Act & Assert
        with patch.dict(os.environ, test_env):
            with pytest.raises(ValueError):
                CacheRepository(mock_redis_connection_handler)
    
    @pytest.mark.asyncio
    async def test_context_manager_usage(self, cache_repository, mock_redis_connection_handler):
        """Test that context manager is properly used"""
        # Arrange
        key = "test_key"
        mapping = {"field1": "value1"}
        mock_redis = AsyncMock()
        mock_redis.hset = AsyncMock()
        mock_redis.expire = AsyncMock()
        mock_redis_connection_handler.__aenter__.return_value = mock_redis
        
        # Act
        await cache_repository.set(key, mapping)
        
        # Assert
        mock_redis_connection_handler.__aenter__.assert_called_once()
        mock_redis_connection_handler.__aexit__.assert_called_once()