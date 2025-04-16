from abc import ABC, abstractmethod

class IStringConnection(ABC):
    
    @property
    @abstractmethod
    def string(self) -> str:pass

    @abstractmethod
    def database_name(self) -> str:pass