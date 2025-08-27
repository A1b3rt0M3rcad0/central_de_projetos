from src.data.interface.i_cache_repository import ICacheRepository
from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
from typing import Dict, Union
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

    async def set(self, key: str, mapping: Union[Dict[str, str], str]) -> bool:
        key = self._ns_key(key)
        async with self.__redis_connection_handler as redis:
            try:
                if isinstance(mapping, dict):
                    # Para dicionários, usa hset
                    await redis.hset(key, mapping=mapping)
                else:
                    # Para strings/valores simples, usa set
                    await redis.set(key, str(mapping))
                await redis.expire(key, self.TTL)
                return True
            except Exception as e:
                raise e from e

    async def get(self, key: str) -> Union[Dict[str, str], str, None]:
        key = self._ns_key(key)
        async with self.__redis_connection_handler as redis:
            try:
                # Primeiro tenta como string (get)
                result = await redis.get(key)
                if result is not None:
                    return result.decode('utf-8') if isinstance(result, bytes) else result
                
                # Se não encontrou como string, tenta como hash (hgetall)
                result = await redis.hgetall(key)
                if result:
                    return result
                
                return None
            except Exception as e:
                # Se deu erro ao tentar como string, tenta como hash
                try:
                    result = await redis.hgetall(key)
                    if result:
                        return result
                except Exception:
                    # Se ambos falharam, levanta a exceção original
                    raise e from e
                
                return None
    
    async def delete(self, key: str) -> bool:
        key = self._ns_key(key)
        async with self.__redis_connection_handler as redis:
            try:
                await redis.delete(key)
                return True
            except Exception as e:
                raise e from e