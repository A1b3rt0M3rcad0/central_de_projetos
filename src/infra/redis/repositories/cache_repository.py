from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
from typing import Dict

class CacheRepository:

    def __init__(self, redis_connection_handler: RedisConnectionHandler):
        self.__redis_connection_handler = redis_connection_handler

    async def set(self, key:str, mapping:Dict[str, str]) -> bool:
        async with self.__redis_connection_handler as redis:
            try:
                await redis.hset(key, mapping=mapping)
                return True
            except Exception as e:
                raise e from e

    async def get(self, key: str) -> Dict[str, str]:
        async with self.__redis_connection_handler as redis:
            try:
                return await redis.hgetall(key)
            except Exception as e:
                raise e from e
    
    async def delete(self, key: str) -> bool:
        async with self.__redis_connection_handler as redis:
            try:
                await redis.delete(key)
                return True
            except Exception as e:
                raise e from e