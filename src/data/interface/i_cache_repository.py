from abc import ABC, abstractmethod
from typing import Dict

class ICacheRepository(ABC):

    @abstractmethod
    def _ns_key(self, key: str) -> str:
        '''
        Namespaces the key by adding the namespace prefix.
        '''

    @abstractmethod
    async def set(self, key: str, mapping: Dict[str, str]) -> bool:
        '''
        Set a value in the cache.
        '''

    @abstractmethod
    async def get(self, key: str) -> Dict[str, str]:
        '''
        Get a value from the cache.
        '''

    @abstractmethod
    async def delete(self, key: str) -> bool:
        '''
        Delete a value from the cache.
        '''