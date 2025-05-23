from src.auth.auth_factory import auth_factory
from src.data.use_cases.encode_jwt import EncodeJwt

def encode_jwt_composer() -> EncodeJwt:
    return EncodeJwt(
        encrypt=auth_factory()
    )