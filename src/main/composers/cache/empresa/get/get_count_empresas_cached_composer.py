from src.infra.redis.config.connection.redis_url_connection import RedisUrlConnection
from src.infra.redis.config.connection.redis_connection_handler import RedisConnectionHandler
from src.infra.redis.repositories.cache_repository import CacheRepository
from src.data.use_cases.get_cached_value import GetCachedValue
from src.presentation.controllers.cache.empresa.get.get_count_empresas_cached_controller import GetCountEmpresasCachedController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_count_empresas_cached_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetCountEmpresasCachedController(
        get_cached_value=GetCachedValue(
            cache_repository=CacheRepository(
                redis_connection_handler=RedisConnectionHandler(
                    redis_url_connection=RedisUrlConnection()
                )
            )
        )
    ).handle 