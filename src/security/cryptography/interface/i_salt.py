from abc import ABC, abstractmethod

class ISalt(ABC):
   
    @staticmethod
    @abstractmethod
    def gen_salt() -> bytes:pass

    @property
    @abstractmethod
    def salt(self) -> bytes:pass