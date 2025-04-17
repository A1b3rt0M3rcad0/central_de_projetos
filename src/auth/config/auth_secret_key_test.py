from src.auth.config.auth_secret_key import AuthSecretKey

def test_secret_key():
    secret_key = AuthSecretKey().secret_key
    assert secret_key is not None
    assert isinstance(secret_key, str)