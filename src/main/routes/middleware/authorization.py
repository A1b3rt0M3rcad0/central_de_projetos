#pylint:disable=R0912,R0915
import dotenv
import os
from datetime import datetime, timedelta, timezone

from fastapi import Request, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from src.domain.value_objects.cpf import CPF
from src.main.composers.internal.decode_jwt_composer import decode_jwt_composer
from src.main.composers.internal.encode_jwt_composer import encode_jwt_composer
from src.main.composers.internal.valid_jwt_composer import valid_jwt_composer
from src.main.composers.internal.find_refresh_token_composer import find_refresh_token_internal_composer


BEARER_SCHEME = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Security(BEARER_SCHEME),
    request: Request = None
):
    if not token or not token.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não encontrado."
        )

    decode_jwt = decode_jwt_composer()
    encode_jwt = encode_jwt_composer()
    valid_jwt = valid_jwt_composer()
    find_refresh_token = find_refresh_token_internal_composer()

    try:
        # Valida token de acesso
        validation = valid_jwt.valid(token.credentials)

        if validation.get("invalid"):
            raise InvalidTokenError("Token inválido.")

        if not validation.get("expired"):
            # Token válido e não expirado
            payload = decode_jwt.decode(token.credentials)

            user_data = {
                "cpf": payload.get("cpf"),
                "role": payload.get("role", []),
                "exp": payload.get("exp")
            }

            if request:
                request.state.user = user_data
                request.state.new_access_token = None

            return user_data

        # Token expirado — verificar se está dentro do deadline
        payload = decode_jwt.decode(token.credentials, verify_exp=False)
        
        # VALIDAÇÃO DO DEADLINE
        deadline = payload.get("deadline")
        if deadline:
            # Converter deadline para datetime se for timestamp
            if isinstance(deadline, (int, float)):
                deadline_datetime = datetime.fromtimestamp(deadline, tz=timezone.utc)
            else:
                deadline_datetime = deadline
            
            # Verificar se passou do deadline
            current_time = datetime.now(timezone.utc)
            if current_time > deadline_datetime:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expirou definitivamente. Deadline ultrapassado. Faça login novamente."
                )
        
        cpf_value = payload.get("cpf")
        if not cpf_value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="CPF não encontrado no token."
            )

        user_cpf = CPF(cpf_value)

        refresh_token_data = find_refresh_token.find(user_cpf=user_cpf)
        if not refresh_token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token não encontrado. Faça login novamente."
            )

        refresh_validation = valid_jwt.valid(refresh_token_data.token)

        if refresh_validation.get("expired"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expirado. Faça login novamente."
            )

        # Gera novo access token com novo deadline
        dotenv.load_dotenv()
        
        # Configurações de tempo do token
        access_token_hours = float(os.getenv('EXPIRE_TIME_TOKEN', '48'))
        deadline_hours = float(os.getenv('EXPIRE_DEADLINE', '24'))
        
        current_time = datetime.now(timezone.utc)
        new_expiry = current_time + timedelta(hours=access_token_hours)
        new_deadline = current_time + timedelta(hours=deadline_hours)
        
        new_access_token = encode_jwt.encode({
            "cpf": payload.get("cpf"),
            "role": payload.get("role"),
            'exp': int(new_expiry.timestamp()),
            'deadline': int(new_deadline.timestamp())
        })

        new_payload = decode_jwt.decode(new_access_token)

        user_data = {
            "cpf": new_payload.get("cpf"),
            "role": new_payload.get("role", []),
            "exp": new_payload.get("exp")
        }

        if request:
            request.state.user = user_data
            request.state.new_access_token = new_access_token

        return user_data

    except (InvalidTokenError, ExpiredSignatureError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Falha na autenticação: {str(e)}"
        ) from e


def role_required(allowed_roles: list[str]):
    """
    Dependência para verificação de roles.
    """
    def role_checker(
        request: Request,
        user: dict = Security(get_current_user)
    ):
        roles = user.get("role", [])
        if isinstance(roles, str):
            roles = [roles]

        if not any(role in allowed_roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Permissão negada."
            )

        request.state.user = user
        return user

    return role_checker