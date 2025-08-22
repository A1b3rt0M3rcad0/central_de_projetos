from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
from src.infra.redis.config.connection.redis_url_connection import RedisUrlConnection
from src.infra.redis.repositories.cache_repository import CacheRepository
from src.data.use_cases.set_cached_value import SetCachedValue
from src.presentation.controllers.cache.bairro.set.set_bairro_by_name_cached_controller import SetBairroByNameCachedController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable


async def set_bairro_by_name_cached_composer() -> Callable[[HttpRequest], HttpResponse]:
    return SetBairroByNameCachedController(
        set_cached_value=SetCachedValue(
            cache_repository=CacheRepository(
                redis_connection_handler=RedisConnectionHandler(
                    redis_url_connection=RedisUrlConnection()
                )
            )
        )
    ).handle