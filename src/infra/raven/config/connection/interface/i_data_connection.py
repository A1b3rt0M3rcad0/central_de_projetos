
from typing import Dict
from abc import ABC, abstractmethod

class IDataConnection(ABC):

    @abstractmethod
    def data(self) -> Dict:pass