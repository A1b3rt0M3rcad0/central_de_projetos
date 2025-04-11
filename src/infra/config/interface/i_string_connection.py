from abc import ABC, abstractmethod

class IStringConnection(ABC):

    @abstractmethod
    def get_connection(self) -> str:pass