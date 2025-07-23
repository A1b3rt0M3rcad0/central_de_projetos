#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_empresa_by_exact_name_composer import find_empresa_by_exact_name_composer
from src.main.composers.find_all_empresas_composer import find_empresas_composer
from src.main.composers.create_empresa_composer import create_empresa_composer
from src.main.composers.delete_empresa_composer import delete_empresa_composer
from src.main.composers.update_empresa_composer import update_empresas_composer
from src.main.composers.count_empresas_composer import count_empresas_composer

from src.main.routes.api.empresa.request_format.create_empresa_format import CreateEmpresaFormat
from src.main.routes.api.empresa.request_format.delete_empresa_format import DeleteEmpresaFormat
from src.main.routes.api.empresa.request_format.update_empresas_composer import UpdateEmpresasFormat
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.empresa.empresa_response.find_empresa_response import FindEmpresaResponse
from src.main.routes.api.empresa.empresa_response.find_all_empresa_response import FindAllEmpresaResponse
from src.main.routes.api.empresa.empresa_response.count_empresas_response import CountEmpresasResponse
from src.main.routes.api.__error.error_response import generate_error_responses

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/empresa'
TAGS = ['empresas']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{empresa_name}', response_model=FindEmpresaResponse, responses=generate_error_responses())
async def find_empresa(empresa_name, request:Request, user=Security(role_required(["VEREADOR", "ADMIN", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_empresa_by_exact_name_composer())
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

@routes.get('/empresa/all', response_model=FindAllEmpresaResponse, responses=generate_error_responses())
async def find_all_empresa(request:Request, user=Security(role_required(["VEREADOR", "ADMIN", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_empresas_composer())
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

@routes.get('/empresa/count/all', response_model=CountEmpresasResponse, responses=generate_error_responses())
async def count_empresas(request:Request, user=Security(role_required(["VEREADOR", "ADMIN", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, count_empresas_composer())
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
async def create_empresa(body:CreateEmpresaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_empresa_composer())
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
async def delete_empresa(body:DeleteEmpresaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_empresa_composer())
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
async def update_empresa(body:UpdateEmpresasFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_empresas_composer())
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