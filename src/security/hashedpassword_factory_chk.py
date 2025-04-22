from src.security.cryptography.blowfish_crypt import BlowfishCrypt
from src.security.cryptography.utils.salt import Salt
from src.security.value_objects.hashed_password import HashedPassword
from src.domain.value_objects.password import Password

def hashedpassword_factory_chk(hashedpassword:bytes, salt:bytes, password:Password) -> bool:
    hashedpassword_obj = HashedPassword(hashedpassword, BlowfishCrypt(), Salt(salt))
    return hashedpassword_obj.check(password)