import dotenv
import os
from datetime import datetime, timedelta, timezone

from fastapi import Request, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from src.domain.value_objects.email import Email
from src.main.composers.internal.decode_jwt_composer import decode_jwt_composer
from src.main.composers.internal.encode_jwt_composer import encode_jwt_composer
from src.main.composers.internal.valid_jwt_composer import valid_jwt_composer
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory


BEARER_SCHEME = HTTPBearer()


def get_current_fiscal(
    token: HTTPAuthorizationCredentials = Security(BEARER_SCHEME),
    request: Request = None
):
    """
    Middleware para autenticação de fiscais mobile.
    Valida o token JWT e verifica se o usuário tem role de FISCAL.
    """
    if not token or not token.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não encontrado."
        )

    decode_jwt = decode_jwt_composer()
    encode_jwt = encode_jwt_composer()
    valid_jwt = valid_jwt_composer()

    try:
        # Valida token de acesso
        validation = valid_jwt.valid(token.credentials)

        if validation.get("invalid"):
            raise InvalidTokenError("Token inválido.")

        if not validation.get("expired"):
            # Token válido e não expirado
            payload = decode_jwt.decode(token.credentials)

            # Verifica se o usuário tem role de fiscal
            role = payload.get("role", "")
            
            if role != "fiscal":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso negado. Apenas fiscais podem acessar este recurso."
                )

            fiscal_data = {
                "email": payload.get("email"),
                "role": payload.get("role", ""),
                "exp": payload.get("exp")
            }

            if request:
                request.state.fiscal = fiscal_data
                request.state.new_access_token = None

            return fiscal_data

        # Token expirado — tenta renovar com refresh token
        payload = decode_jwt.decode(token.credentials, verify_exp=False)
        email_value = payload.get("email")
        if not email_value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email não encontrado no token."
            )

        # Para fiscais, o refresh_token está na tabela fiscal
        # Vamos usar o fiscal repository para encontrar o fiscal pelo email
        fiscal_repository = FiscalRepository(db_connection_handler_factory())
        fiscal_entity = fiscal_repository.find_by_email(Email(email_value))
        
        if not fiscal_entity.refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token não encontrado. Faça login novamente."
            )
        
        refresh_token_data = type('obj', (object,), {'token': fiscal_entity.refresh_token})()

        refresh_validation = valid_jwt.valid(refresh_token_data.token)

        if refresh_validation.get("expired"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expirado. Faça login novamente."
            )

        # Gera novo access token
        dotenv.load_dotenv()
        hours = float(os.getenv('EXPIRE_TIME_TOKEN'))
        new_access_token = encode_jwt.encode({
            "email": payload.get("email"),
            "role": payload.get("role"),
            'exp': datetime.now(timezone.utc) + timedelta(hours=hours)
        })

        new_payload = decode_jwt.decode(new_access_token)

        # Verifica se o usuário tem role de fiscal no novo token
        role = new_payload.get("role", "")
        
        if role != "fiscal":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado. Apenas fiscais podem acessar este recurso."
            )

        fiscal_data = {
            "email": new_payload.get("email"),
            "role": new_payload.get("role", ""),
            "exp": new_payload.get("exp")
        }

        if request:
            request.state.fiscal = fiscal_data
            request.state.new_access_token = new_access_token

        return fiscal_data

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


def fiscal_required():
    """
    Dependência para verificação de autorização de fiscal.
    """
    def fiscal_checker(
        request: Request,
        fiscal: dict = Security(get_current_fiscal)
    ):
        request.state.fiscal = fiscal
        return fiscal

    return fiscal_checker
