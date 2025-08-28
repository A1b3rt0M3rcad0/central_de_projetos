from abc import ABC, abstractmethod
from typing import Dict, Union

class ICacheRepository(ABC):

    @abstractmethod
    def _ns_key(self, key: str) -> str:
        '''
        Namespaces the key by adding the namespace prefix.
        '''

    @abstractmethod
    async def set(self, key: str, mapping: Union[Dict[str, str], str]) -> bool:
        '''
        Set a value in the cache.
        '''

    @abstractmethod
    async def get(self, key: str) -> Union[Dict[str, str], str, None]:
        '''
        Get a value from the cache.
        '''

    @abstractmethod
    async def delete(self, key: str) -> bool:
        '''
        Delete a value from the cache.
        '''