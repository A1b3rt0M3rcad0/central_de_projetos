from src.security.value_objects.interface.i_hashed_password import IHashedPassword
from src.domain.value_objects.password import Password
from src.security.cryptography.interface.i_cryptography import ICryptography
from src.security.cryptography.interface.i_salt import ISalt

class HashedPassword(IHashedPassword):

    def __init__(self, password: Password | bytes, cryptography: ICryptography, salt: ISalt) -> None:
        self.__salt = salt
        self.__cryptography = cryptography
        self.__hashed_password = self.__cryptography.hash(password, self.__salt) if isinstance(password, Password) else password

    @property
    def hashed_password(self) -> bytes:
        return self.__hashed_password
    
    @property
    def salt(self) -> bytes:
        return self.__salt.salt
    
    @property
    def cryptography(self) -> ICryptography:
        return self.__cryptography
    
    def __str__(self) -> str:
        return self.hashed_password.decode()
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.hashed_password.decode()})'