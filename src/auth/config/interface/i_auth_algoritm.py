from abc import ABC, abstractmethod


class IAuthAlgoritm(ABC):

    @property
    @abstractmethod
    def algoritm(self) -> str: pass
    
    @abstractmethod
    def _get_algoritm(self) -> str: pass