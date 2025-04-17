from abc import ABC, abstractmethod
from src.security.cryptography.interface.i_cryptography import ICryptography
from src.security.cryptography.interface.i_salt import ISalt

class IHashedPassword(ABC):

    @property
    @abstractmethod
    def hashed_password(self) -> bytes:pass

    @property
    @abstractmethod
    def salt(self) -> ISalt:pass

    @property
    @abstractmethod
    def cryptography(self) -> ICryptography:pass