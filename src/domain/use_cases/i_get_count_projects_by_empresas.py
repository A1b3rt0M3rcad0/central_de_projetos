from abc import ABC, abstractmethod
from typing import Dict

class IGetCountProjectsByEmpresas(ABC):

    @abstractmethod
    def get(self) -> Dict[str, int]:pass