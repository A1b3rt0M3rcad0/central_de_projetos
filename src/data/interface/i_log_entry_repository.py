from abc import ABC, abstractmethod
from typing import List

class ILogEntryRepository(ABC):

    @abstractmethod
    def save(self, log:"LogEntryModel") -> None:
        ...
    
    @abstractmethod
    def find_all(self, limit:int=100) -> List["LogEntryModel"]:
        ...