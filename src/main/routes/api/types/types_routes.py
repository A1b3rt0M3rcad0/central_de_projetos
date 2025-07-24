#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_type_composer import create_type_composer
from src.main.composers.delete_type_composer import delete_type_composer
from src.main.composers.find_type_by_exact_name_composer import find_type_by_exact_name_composer
from src.main.composers.update_type_composer import update_type_composer
from src.main.composers.find_all_types_composer import find_all_types_composer

from src.main.routes.api.types.request_format.create_type_format import CreateTypeFormat
from src.main.routes.api.types.request_format.delete_type_format import DeleteTypeFormat
from src.main.routes.api.types.request_format.update_type_format import UpdateTypeFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.types.types_response.find_type_by_exact_name_response import FindTypeByExactNameReponse
from src.main.routes.api.types.types_response.find_all_types_response import FindAllTypesResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/types'
TAGS = ['type']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.post('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_type(body:CreateTypeFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_type_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.delete('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def delete_type(body:DeleteTypeFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_type_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.patch('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_type(body:UpdateTypeFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_type_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.get('/find_by_name/{type_name}', response_model=FindTypeByExactNameReponse, responses=generate_error_responses())
async def find_type_by_exact_name(type_name:str, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['type_name'] = type_name
        http_response = await request_adapter(request, find_type_by_exact_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.get('/all', response_model=FindAllTypesResponse, responses=generate_error_responses())
async def find_all_types(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_types_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)