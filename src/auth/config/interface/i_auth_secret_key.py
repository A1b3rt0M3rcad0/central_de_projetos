from abc import ABC, abstractmethod

class IAuthSecretKey(ABC):

    @property
    @abstractmethod
    def secret_key(self) -> str:pass

    @abstractmethod
    def _get_secret_key(self) -> str:pass