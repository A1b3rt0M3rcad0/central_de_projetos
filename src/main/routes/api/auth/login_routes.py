#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.login_composer import login_composer
from src.main.composers.login_fiscal_composer import login_fiscal_composer

from src.main.routes.api.auth.request_format.login_format import LoginFormat
from src.main.routes.api.auth.request_format.login_fiscal_format import LoginFiscalFormat
from src.main.routes.api.auth.response_format.login_response import LoginResponse
from src.main.routes.api.__error.error_response import generate_error_responses

#Limiter
from src.main.routes.middleware.rate_limit import limiter

# Logger
from src.logs.log_http import log_http

PREFIX = '/auth'
TAGS = ['auth', 'login']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.post('/login', response_model=LoginResponse, responses=generate_error_responses())
@limiter.limit("5/minute")
async def login(body:LoginFormat, request:Request):
    try:
        http_response = await request_adapter(request, login_composer())
        LoginResponse(**http_response.body)
        log_http(
            logger_name=PREFIX,
            level="INFO",
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            logger_name=PREFIX,
            level="ERROR",
            http_response=error_result,
            request=request,
        )
        return response_adapter(error_result)
@routes.post('/login/fiscal', response_model=LoginResponse, responses=generate_error_responses())
@limiter.limit("5/minute")
async def login_fiscal(body:LoginFiscalFormat, request:Request):
    """
    Endpoint para login do fiscal via API.
    
    Args:
        body: Dados de login (email e senha)
        request: Objeto da requisição HTTP
        
    Returns:
        LoginResponse: Token JWT e mensagem de sucesso
        
    Raises:
        FiscalNotFoundError: Se o fiscal não for encontrado
        InvalidPasswordError: Se a senha estiver incorreta
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, login_fiscal_composer())
        LoginResponse(**http_response.body)
        log_http(
            logger_name=PREFIX,
            level="INFO",
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            logger_name=PREFIX,
            level="ERROR",
            http_response=error_result,
            request=request,
        )
        return response_adapter(error_result)
