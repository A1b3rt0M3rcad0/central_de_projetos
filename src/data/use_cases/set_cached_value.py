from src.data.interface.i_cache_repository import ICacheRepository
from src.domain.use_cases.i_set_cached_value import ISetCachedValue

class SetCachedValue(ISetCachedValue):
    def __init__(self, cache_repository: ICacheRepository):
        self.cache_repository = cache_repository

    async def set(self, key: str, value: str) -> None:
        await self.cache_repository.set(key, value)