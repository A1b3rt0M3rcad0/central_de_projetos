from abc import ABC, abstractmethod
from src.security.cryptography.interface.i_salt import ISalt
from src.domain.value_objects.password import Password

class ICryptography(ABC):

    @staticmethod
    @abstractmethod
    def hash(password:Password, salt:ISalt) -> bytes:pass

    @staticmethod
    @abstractmethod
    def check(password:Password, hashed_password:bytes) -> bool:pass