#pylint:disable=all
import pytest
import os
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
from src.infra.redis.config.connection.redis_url_connection import RedisUrlConnection

class TestRedisConnectionHandler:
    
    def setup_method(self):
        """Setup method to clear environment variables before each test"""
        # Clear Redis environment variables
        env_vars = ['REDIS_NAMESPACE']
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]
    
    @pytest.fixture
    def mock_redis_url_connection(self):
        """Fixture to create a mock RedisUrlConnection"""
        mock_connection = Mock(spec=RedisUrlConnection)
        mock_connection.url = 'localhost'
        mock_connection.port = 6379
        mock_connection.username = 'test_user'
        mock_connection.password = 'test_password'
        mock_connection.decode_responses = True
        mock_connection.socket_connect_timeout = 5.0
        mock_connection.socket_timeout = 10.0
        return mock_connection
    
    @pytest.fixture
    def redis_connection_handler(self, mock_redis_url_connection):
        """Fixture to create a RedisConnectionHandler instance"""
        return RedisConnectionHandler(mock_redis_url_connection)
    
    def test_init_with_default_namespace(self, mock_redis_url_connection):
        """Test initialization with default namespace"""
        # Arrange - Clear REDIS_NAMESPACE to test default
        with patch.dict(os.environ, {}, clear=True):
            with patch('src.infra.redis.config.connection.redis_connection_handler.load_dotenv'):
                # Act
                handler = RedisConnectionHandler(mock_redis_url_connection)
                
                # Assert
                assert handler.NAMESPACE == "DEFAULT"
                assert handler._RedisConnectionHandler__redis_url_connection == mock_redis_url_connection
                assert handler._RedisConnectionHandler__redis is None
    
    def test_init_with_custom_namespace(self, mock_redis_url_connection):
        """Test initialization with custom namespace"""
        # Arrange
        test_env = {'REDIS_NAMESPACE': 'test_app'}
        
        # Act
        with patch.dict(os.environ, test_env):
            handler = RedisConnectionHandler(mock_redis_url_connection)
        
        # Assert
        assert handler.NAMESPACE == "TEST_APP"
    
    @pytest.mark.asyncio
    async def test_aenter_successful_connection(self, redis_connection_handler, mock_redis_url_connection):
        """Test successful connection establishment"""
        # Arrange
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock()
        
        with patch('src.infra.redis.config.connection.redis_connection_handler.Redis', return_value=mock_redis):
            # Act
            async with redis_connection_handler as redis:
                # Assert
                assert redis == mock_redis
                mock_redis.ping.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_aenter_connection_failure(self, redis_connection_handler, mock_redis_url_connection):
        """Test connection failure during establishment"""
        # Arrange
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock(side_effect=Exception("Connection failed"))
        mock_redis.aclose = AsyncMock()
        
        with patch('src.infra.redis.config.connection.redis_connection_handler.Redis', return_value=mock_redis):
            # Act & Assert
            with pytest.raises(Exception, match="Connection failed"):
                async with redis_connection_handler as redis:
                    pass
            
            # Verify cleanup was called
            mock_redis.aclose.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_aenter_connection_failure_with_cleanup_exception(self, redis_connection_handler, mock_redis_url_connection):
        """Test connection failure with cleanup exception"""
        # Arrange
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock(side_effect=Exception("Connection failed"))
        mock_redis.aclose = AsyncMock(side_effect=Exception("Cleanup failed"))
        
        with patch('src.infra.redis.config.connection.redis_connection_handler.Redis', return_value=mock_redis):
            # Act & Assert
            with pytest.raises(Exception, match="Cleanup failed"):
                async with redis_connection_handler as redis:
                    pass
            
            # Verify cleanup was attempted
            mock_redis.aclose.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_aexit_successful_cleanup(self, redis_connection_handler, mock_redis_url_connection):
        """Test successful cleanup on exit"""
        # Arrange
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock()
        mock_redis.aclose = AsyncMock()
        
        with patch('src.infra.redis.config.connection.redis_connection_handler.Redis', return_value=mock_redis):
            # Act
            async with redis_connection_handler as redis:
                pass
            
            # Assert
            mock_redis.aclose.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_aexit_with_no_redis_connection(self, redis_connection_handler, mock_redis_url_connection):
        """Test exit when no Redis connection exists"""
        # Arrange
        redis_connection_handler._RedisConnectionHandler__redis = None
        
        # Act
        result = await redis_connection_handler.__aexit__(None, None, None)
        
        # Assert
        assert result is False
    
    @pytest.mark.asyncio
    async def test_redis_connection_parameters(self, mock_redis_url_connection):
        """Test that Redis connection is created with correct parameters"""
        # Arrange - Clear environment to get default namespace
        with patch.dict(os.environ, {}, clear=True):
            with patch('src.infra.redis.config.connection.redis_connection_handler.load_dotenv'):
                handler = RedisConnectionHandler(mock_redis_url_connection)
                
                with patch('src.infra.redis.config.connection.redis_connection_handler.Redis') as mock_redis_class:
                    mock_redis_instance = AsyncMock()
                    mock_redis_instance.ping = AsyncMock()
                    mock_redis_class.return_value = mock_redis_instance
                    
                    # Act
                    async with handler as redis:
                        pass
                    
                    # Assert
                    mock_redis_class.assert_called_once_with(
                        client_name="DEFAULT",
                        host='localhost',
                        port=6379,
                        username='test_user',
                        password='test_password',
                        decode_responses=True,
                        socket_connect_timeout=5.0,
                        socket_timeout=10.0
                    )
    
    @pytest.mark.asyncio
    async def test_connection_timeout_handling(self, redis_connection_handler, mock_redis_url_connection):
        """Test handling of connection timeout"""
        # Arrange
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock(side_effect=asyncio.TimeoutError("Connection timeout"))
        mock_redis.aclose = AsyncMock()
        
        with patch('src.infra.redis.config.connection.redis_connection_handler.Redis', return_value=mock_redis):
            # Act & Assert
            with pytest.raises(asyncio.TimeoutError, match="Connection timeout"):
                async with redis_connection_handler as redis:
                    pass
            
            # Verify cleanup was called
            mock_redis.aclose.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_multiple_connections_same_handler(self, redis_connection_handler, mock_redis_url_connection):
        """Test multiple connections using the same handler"""
        # Arrange
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock()
        mock_redis.aclose = AsyncMock()
        
        with patch('src.infra.redis.config.connection.redis_connection_handler.Redis', return_value=mock_redis):
            # Act
            async with redis_connection_handler as redis1:
                pass
            
            async with redis_connection_handler as redis2:
                pass
            
            # Assert
            assert mock_redis.aclose.call_count == 2
    
    def test_namespace_uppercase_conversion(self, mock_redis_url_connection):
        """Test that namespace is converted to uppercase"""
        # Arrange
        test_env = {'REDIS_NAMESPACE': 'my_app'}
        
        # Act
        with patch.dict(os.environ, test_env):
            handler = RedisConnectionHandler(mock_redis_url_connection)
        
        # Assert
        assert handler.NAMESPACE == "MY_APP" 