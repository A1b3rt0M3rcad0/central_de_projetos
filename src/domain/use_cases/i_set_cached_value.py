from abc import ABC, abstractmethod

class ISetCachedValue(ABC):

    @abstractmethod
    async def set(self, key: str, value: str) -> None:
        pass