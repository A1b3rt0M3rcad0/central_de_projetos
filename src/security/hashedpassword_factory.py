from src.security.cryptography.blowfish_crypt import BlowfishCrypt
from src.security.cryptography.utils.salt import Salt
from src.security.value_objects.hashed_password import HashedPassword
from src.domain.value_objects.password import Password

def hashedpassword_factory(password:Password) -> HashedPassword:
    return HashedPassword(password, BlowfishCrypt(), Salt())