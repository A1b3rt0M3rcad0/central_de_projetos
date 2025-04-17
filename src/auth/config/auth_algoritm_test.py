from src.auth.config.auth_algoritm import AuthAlgoritm

def test_auth_algoritm():
    algoritm = AuthAlgoritm().algoritm
    assert algoritm is not None
    assert isinstance(algoritm, str)