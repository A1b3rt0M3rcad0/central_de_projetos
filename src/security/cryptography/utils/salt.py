from src.security.cryptography.interface.i_salt import ISalt
import bcrypt

class Salt(ISalt):

    def __init__(self, salt:bytes|None=None) -> None:
        if salt is None:
            self.__salt = self.gen_salt()
        else:
            self.__salt = salt

    @staticmethod
    def gen_salt() -> bytes:
        return bcrypt.gensalt()
    
    @property
    def salt(self) -> bytes:
        return self.__salt