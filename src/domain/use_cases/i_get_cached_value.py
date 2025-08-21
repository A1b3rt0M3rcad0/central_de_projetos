from abc import ABC, abstractmethod

class IGetCachedValue(ABC):

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """
        Get a cached value by key in Redis.
        """