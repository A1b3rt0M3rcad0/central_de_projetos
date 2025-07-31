#pylint:disable=W0718
#pylint:disable=W0613,W0012,W9016
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_fiscal_by_name_composer import find_fiscal_by_name_composer
from src.main.composers.create_fiscal_composer import create_fiscal_composer
from src.main.composers.delete_fiscal_composer import delete_fiscal_composer
from src.main.composers.update_fiscal_name_composer import update_fiscal_name_composer
from src.main.composers.find_all_fiscal_composer import find_all_fiscal_composer
from src.main.composers.count_fiscals_composer import count_fiscals_composer
from src.main.composers.insert_all_fiscal_from_user_composer import insert_all_fiscal_from_user_composer

from src.main.routes.api.fiscal.request_format.create_fiscal_format import CreateFiscalFormat
from src.main.routes.api.fiscal.request_format.delete_fiscal_format import DeleteFiscalFormat
from src.main.routes.api.fiscal.request_format.update_fiscal_name_format import UpdateFiscalNameFormat
from src.main.routes.api.fiscal.request_format.insert_all_fiscal_from_user_format import InsertAllFiscalFromUserFormat
from src.main.routes.api.fiscal.fiscal_response.find_fiscal_by_name_response import FindFiscalByNameResponse
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.fiscal.fiscal_response.find_all_fiscal_response import FindAllFiscalReponse
from src.main.routes.api.fiscal.fiscal_response.count_fiscal_response import CountFiscalReponse
from src.main.routes.api.__error.error_response import generate_error_responses

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/fiscal'
TAGS = ['fiscal']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{fiscal_name}', response_model=FindFiscalByNameResponse, responses=generate_error_responses())
async def find_fiscal_by_name(fiscal_name, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['fiscal_name'] = fiscal_name
        http_response = await request_adapter(request, find_fiscal_by_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
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

@routes.get('/fiscal/all', response_model=FindAllFiscalReponse, responses=generate_error_responses())
async def find_all_fiscal(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_fiscal_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
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

@routes.get('/fiscal/count/all', response_model=CountFiscalReponse, responses=generate_error_responses())
async def count_fiscals(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, count_fiscals_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
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

@routes.post('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_fiscal(body:CreateFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_fiscal_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
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

@routes.delete('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def delete_fiscal(body:DeleteFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_fiscal_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
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

@routes.patch('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_fiscal(body:UpdateFiscalNameFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_fiscal_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
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

@routes.post('/insert-all', response_model=BaseMessageResponse, responses=generate_error_responses())
async def insert_all_fiscal_from_user(body:InsertAllFiscalFromUserFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para inserir fiscal com todos os dados (nome, email, senha, telefone).
    Apenas ADMIN pode acessar este endpoint.
    
    Args:
        body: Dados do fiscal (nome, email, senha, telefone)
        request: Objeto da requisição HTTP
        user: Usuário autenticado (deve ser ADMIN)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso
        
    Raises:
        FiscalAlreadyExists: Se o fiscal já existe
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, insert_all_fiscal_from_user_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
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