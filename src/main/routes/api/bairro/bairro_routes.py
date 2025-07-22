#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_bairro_by_name_composer import find_bairro_by_name_composer
from src.main.composers.create_bairro_composer import create_bairro_composer
from src.main.composers.delete_bairro_composer import delete_bairro_composer
from src.main.composers.update_bairro_name_composer import update_bairro_name_composer
from src.main.composers.find_all_bairro_composer import find_all_bairro_composer
from src.main.composers.count_bairros_composer import count_bairros_composer

from src.main.routes.api.bairro.request_format.create_bairro_format import CreateBairroFormat
from src.main.routes.api.bairro.request_format.delete_bairro_format import DeleteBairroFormat
from src.main.routes.api.bairro.request_format.update_bairro_name_format import UpdateBairroNameFormat

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

## Logs
from src.logs.log_http import log_http

PREFIX = '/bairro'
TAGS = ['bairros']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{bairro_name}')
async def find_bairro_by_name(bairro_name:str, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_bairro_by_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            http_response=http_response,
            level='INFO',
            logger_name=PREFIX,
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

@routes.get('/count/all')
async def count_bairros(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, count_bairros_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            logger_name=PREFIX,
            level='INFO',
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response)

    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.get('/bairro/all')
async def find_all_bairro(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_bairro_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            request=request,
            logger_name=PREFIX,
            http_response=http_response
        )
        return response_adapter(http_response)

    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.post('/')
async def create_bairro(body:CreateBairroFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_bairro_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.delete('/')
async def delete_bairro(body:DeleteBairroFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_bairro_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.patch('/name')
async def update_bairro_name(body:UpdateBairroNameFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_bairro_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response) 
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)