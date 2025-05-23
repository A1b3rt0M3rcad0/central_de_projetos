from abc import ABC, abstractmethod
from typing import Dict

class IDecodeJwtToken(ABC):

    @abstractmethod
    def decode(self, token:str, verify_exp=True) -> Dict:
        '''Retorna o dicionario do token decoded'''