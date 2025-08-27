from src.data.interface.i_cache_repository import ICacheRepository
from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
from typing import Dict
from dotenv import load_dotenv
import os

class CacheRepository(ICacheRepository):

    
    def __init__(self, redis_connection_handler: RedisConnectionHandler):
        load_dotenv()
        self.__redis_connection_handler = redis_connection_handler
        self.NAMESPACE = os.getenv("REDIS_NAMESPACE", "default").upper() + ':'
        self.TTL = int(os.getenv("REDIS_TTL", '360'))

    def _ns_key(self, key: str) -> str:
        return f"{self.NAMESPACE}{key}"

    async def set(self, key:str, mapping:Dict[str, str]) -> bool:
        key = self._ns_key(key)
        async with self.__redis_connection_handler as redis:
            try:
                await redis.hset(key, mapping=mapping)
                await redis.expire(key, self.TTL)
                return True
            except Exception as e:
                raise e from e

    async def get(self, key: str) -> Dict[str, str]:
        key = self._ns_key(key)
        async with self.__redis_connection_handler as redis:
            try:
                return await redis.hgetall(key)
            except Exception as e:
                raise e from e
    
    async def delete(self, key: str) -> bool:
        key = self._ns_key(key)
        async with self.__redis_connection_handler as redis:
            try:
                await redis.delete(key)
                return True
            except Exception as e:
                raise e from e