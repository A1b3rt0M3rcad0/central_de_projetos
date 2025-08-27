from src.infra.redis.config.connection.redis_url_connection import RedisUrlConnection
from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
from src.infra.redis.repositories.cache_repository import CacheRepository
from src.data.use_cases.set_cached_value import SetCachedValue
from src.presentation.controllers.cache.project.set.set_project_detail_cached_controller import SetProjectDetailCachedController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def set_project_detail_cached_composer() -> Callable[[HttpRequest], HttpResponse]:
    return SetProjectDetailCachedController(
        set_cached_value=SetCachedValue(
            cache_repository=CacheRepository(
                redis_connection_handler=RedisConnectionHandler(
                    redis_url_connection=RedisUrlConnection()
                )
            )
        )
    ).handle 