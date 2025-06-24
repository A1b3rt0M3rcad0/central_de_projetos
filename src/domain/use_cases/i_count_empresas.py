from abc import ABC, abstractmethod
from typing import Dict

class ICountEmpresas(ABC):

    @abstractmethod
    def count(self) -> Dict[str, int]:pass