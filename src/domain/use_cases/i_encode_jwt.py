from abc import ABC, abstractmethod
from typing import Dict

class IEncodeJwt(ABC):

    @abstractmethod
    def encode(self, payload:Dict) -> str:
        '''
        Faz o encode do payload
        '''