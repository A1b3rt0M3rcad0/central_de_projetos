from abc import ABC, abstractmethod

class IEncrypt(ABC):

    @abstractmethod
    def encode(self, payload: dict) -> str:
        pass

    @abstractmethod
    def decode(self, token: str, verify_exp=True) -> dict:
        pass

    @abstractmethod
    def is_expired(self, token:str) -> dict:
        pass