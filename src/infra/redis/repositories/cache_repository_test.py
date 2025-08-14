from src.infra.redis.config.connection.redis_url_connection import RedisUrlConnection
from src.infra.redis.repositories.cache_repository import CacheRepository
from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
import pytest

@pytest.fixture
def cache_repository():
    redis_connection_handler = RedisConnectionHandler(RedisUrlConnection())
    return CacheRepository(redis_connection_handler)

@pytest.mark.skip('Skipping test_cache_repository_set')
@pytest.mark.asyncio
async def test_cache_repository_set(cache_repository):
    result = await cache_repository.set("test_key", {"field1": "value1", "field2": "value2"})
    assert result is True

@pytest.mark.skip('Skipping test_cache_repository_get')
@pytest.mark.asyncio
async def test_cache_repository_get(cache_repository):
    await cache_repository.set("test_key", {"field1": "value1", "field2": "value2"})
    result = await cache_repository.get("test_key")
    assert result == {"field1": "value1", "field2": "value2"}

@pytest.mark.skip('Skipping test_cache_repository_delete')
@pytest.mark.asyncio
async def test_cache_repository_delete(cache_repository):
    await cache_repository.set("test_key", {"field1": "value1", "field2": "value2"})
    result = await cache_repository.delete("test_key")
    assert result is True