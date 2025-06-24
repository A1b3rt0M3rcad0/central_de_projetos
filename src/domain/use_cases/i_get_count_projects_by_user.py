from typing import Dict
from abc import ABC, abstractmethod

class IGetCountProjectsByuser(ABC):

    @abstractmethod
    def get(self) -> Dict[str, int]:pass