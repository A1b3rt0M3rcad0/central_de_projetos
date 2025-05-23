from src.auth.auth_factory import auth_factory
from src.data.use_cases.valid_jwt import ValidJwt

def valid_jwt_composer() -> ValidJwt:
    return ValidJwt(encrypt=auth_factory())