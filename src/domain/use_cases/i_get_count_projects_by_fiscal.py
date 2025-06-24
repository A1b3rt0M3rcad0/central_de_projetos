from abc import ABC, abstractmethod
from typing import Dict

class IGetCountProjectsByFiscal(ABC):

    @abstractmethod
    def get(self) -> Dict[str, int]:pass