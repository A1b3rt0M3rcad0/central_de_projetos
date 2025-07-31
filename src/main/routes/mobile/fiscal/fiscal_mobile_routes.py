#pylint:disable=W0611, W0613
from fastapi import APIRouter, Request, Security
from datetime import datetime
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.errors.error_handle import error_handler
from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.middleware.insert_access_token import insert_access_token
from src.main.routes.middleware.fiscal_authorization import fiscal_required
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.composers.login_fiscal_composer import login_fiscal_composer
from src.main.routes.mobile.fiscal.request_format.login_fiscal_format import LoginFiscalFormat
from src.main.routes.mobile.fiscal.response_format.login_fiscal_response import LoginFiscalResponse
from src.main.routes.mobile.fiscal.response_format.test_fiscal_response import FiscalTestResponse
from src.logs.log_http import log_http

PREFIX = '/mobile/fiscal'

routes = APIRouter(prefix=PREFIX, tags=['Fiscal Mobile'])

@routes.post('/login', 
             response_model=LoginFiscalResponse, 
             responses=generate_error_responses())
async def login_fiscal_mobile(
    body: LoginFiscalFormat, 
    request: Request
):
    """
    Endpoint para login do fiscal via aplicativo mobile.
    
    Args:
        body: Dados de login (email e senha)
        request: Objeto da requisição HTTP
        
    Returns:
        LoginFiscalResponse: Token JWT e mensagem de sucesso
        
    Raises:
        FiscalNotFoundError: Se o fiscal não for encontrado
        InvalidPasswordError: Se a senha estiver incorreta
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, login_fiscal_composer())
        
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)


@routes.get('/test', 
            response_model=FiscalTestResponse, 
            responses=generate_error_responses())
async def test_fiscal_mobile(
    request: Request,
    fiscal: dict = Security(fiscal_required())
):
    """
    Endpoint de teste para verificar se o fiscal está autenticado.
    
    Args:
        request: Objeto da requisição HTTP
        fiscal: Dados do fiscal autenticado (injetado pelo middleware)
        
    Returns:
        TestFiscalResponse: Dados do fiscal autenticado e timestamp
        
    Raises:
        HTTPException: Se o fiscal não estiver autenticado ou não tiver permissão
    """
    try:
        # Obtém os dados do fiscal do request.state
        fiscal_data = request.state.fiscal
        
        response_data = {
            "message": "Fiscal autenticado com sucesso!",
            "fiscal_email": fiscal_data.get("email", ""),
            "fiscal_role": fiscal_data.get("role", ""),
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response={"status_code": 200, "body": response_data},
            request=request
        )
        
        return response_data
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)