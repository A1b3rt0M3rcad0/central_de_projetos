from src.auth.auth_factory import auth_factory
from src.data.use_cases.decode_jwt_token import DecodeJwtToken

def decode_jwt_composer() -> DecodeJwtToken:
    return DecodeJwtToken(
        encrypt=auth_factory()
    )