from fastapi import Request, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.main.composers.internal.decode_jwt_composer import decode_jwt_composer

BEARER_SCHEME = HTTPBearer()

def get_current_user(
    token: HTTPAuthorizationCredentials = Security(BEARER_SCHEME),
    request: Request = None
):
    if not token or not token.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não encontrado")

    try:
        decode_jwt = decode_jwt_composer()
        payload = decode_jwt.decode(token.credentials)

        # Guardar o user no request.state para outras funções
        if request is not None:
            request.state.user = {
                "cpf": payload.get("cpf"),
                "role": payload.get("role", []),
                "exp": payload.get("exp")
            }

        return {
            "cpf": payload.get("cpf"),
            "role": payload.get("role", []),
            "exp": payload.get("exp")
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


def role_required(allowed_roles: list[str]):
    def role_checker(
        token: HTTPAuthorizationCredentials = Security(BEARER_SCHEME)
    ):
        decode_jwt = decode_jwt_composer()
        payload = decode_jwt.decode(token.credentials)
        
        roles = payload.get("role", [])
        if isinstance(roles, str):
            roles = [roles]

        if not any(role in allowed_roles for role in roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada")
        return payload
    return role_checker
