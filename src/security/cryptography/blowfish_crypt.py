from src.security.cryptography.interface.i_cryptography import ICryptography
from src.security.cryptography.interface.i_salt import ISalt
from src.domain.value_objects.password import Password
import bcrypt


class BlowfishCrypt(ICryptography):
    
    @staticmethod
    def hash(password:Password, salt:ISalt) -> bytes:
        salt_bytes = salt.salt
        password = password.password
        return bcrypt.hashpw(password.encode(), salt_bytes)
    
    @staticmethod
    def check(password:Password, hashed_password:bytes) -> bool:
        password = password.password
        return bcrypt.checkpw(password.encode(), hashed_password)