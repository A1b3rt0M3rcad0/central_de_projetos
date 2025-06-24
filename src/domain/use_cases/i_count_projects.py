from abc import ABC, abstractmethod
from typing import Dict

class ICountProjects(ABC):

    @abstractmethod
    def count(self) -> Dict[str, int]:pass