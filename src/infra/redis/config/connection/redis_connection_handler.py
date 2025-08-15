from src.infra.redis.config.connection.redis_url_connection import RedisUrlConnection
from redis.asyncio import Redis
from typing import Optional
import asyncio
import os
from dotenv import load_dotenv

class RedisConnectionHandler:
    def __init__(self, redis_url_connection: RedisUrlConnection) -> None:
        load_dotenv()
        self.__redis_url_connection: RedisUrlConnection = redis_url_connection
        self.__redis: Optional[Redis] = None
        self.NAMESPACE = os.getenv("REDIS_NAMESPACE", "default").upper()

    async def __aenter__(self) -> Redis:
        self.__redis = Redis(
            client_name=self.NAMESPACE,
            host=self.__redis_url_connection.url,
            port=self.__redis_url_connection.port,
            username=self.__redis_url_connection.username,
            password=self.__redis_url_connection.password,
            decode_responses=self.__redis_url_connection.decode_responses,
            socket_connect_timeout=self.__redis_url_connection.socket_connect_timeout,
            socket_timeout=self.__redis_url_connection.socket_timeout
        )
        try:
            await asyncio.wait_for(self.__redis.ping(), timeout=self.__redis_url_connection.socket_timeout)
        except Exception:
            try:
                await self.__redis.aclose()
            finally:
                self.__redis = None
            raise
        return self.__redis

    async def __aexit__(self, exc_type, exc_value, traceback) -> bool:
        if self.__redis is not None:
            await self.__redis.aclose()
            self.__redis = None
        return False


if __name__ == "__main__":
    async def main():
        """Função principal para teste"""
        redis_url_connection = RedisUrlConnection()
        async with RedisConnectionHandler(redis_url_connection) as redis:
            await redis.set("test", "test")
            result = await redis.get("test")
            print(result)
    asyncio.run(main())