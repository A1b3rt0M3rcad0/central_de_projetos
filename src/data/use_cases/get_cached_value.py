from src.data.interface.i_cache_repository import ICacheRepository
from src.domain.use_cases.i_get_cached_value import IGetCachedValue

class GetCachedValue(IGetCachedValue):

    def __init__(self, cache_repository: ICacheRepository):
        self.cache_repository = cache_repository

    async def get(self, key: str) -> str | None:
        return await self.cache_repository.get(key)
