from src.auth.auth_factory import auth_factory
from src.auth.encrypt.encrypt import Encrypt

def test_auth_factory():
    auth = auth_factory()
    assert auth is not None
    assert isinstance(auth, Encrypt)