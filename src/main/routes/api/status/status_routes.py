#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_status_composer import find_status_composer
from src.main.composers.create_status_composer import create_status_composer
from src.main.composers.delete_status_composer import delete_status_composer
from src.main.composers.update_status_description_composer import update_status_description_composer
from src.main.composers.find_all_status_composer import find_all_status_composer
from src.main.composers.find_project_by_status_composer import find_project_by_status_composer

from src.main.routes.api.status.format_request.create_status_format import CreateStatusFormat
from src.main.routes.api.status.format_request.delete_status_format import DeleteStatusFormat
from src.main.routes.api.status.format_request.update_status_description_format import UpdateStatusDescriptionFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.status.status_response.find_status_response import FindStatusReponse
from src.main.routes.api.status.status_response.find_all_status_response import FindAllStatusResponse
from src.main.routes.api.status.status_response.find_project_by_status_response import FindProjectbyStatusReponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/status'
TAGS = ['status']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{status_id}', response_model=FindStatusReponse, responses=generate_error_responses())
async def find_status(status_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['status_id'] = status_id
        http_response = await request_adapter(request, find_status_composer())
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

@routes.post('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_status(body:CreateStatusFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_status_composer())
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
async def delete_status(body:DeleteStatusFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_status_composer())
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
async def update_status_description(body:UpdateStatusDescriptionFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_status_description_composer())
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
    
@routes.get('/status/all/', response_model=FindAllStatusResponse, responses=generate_error_responses())
async def find_all_status(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_status_composer())
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

@routes.get('/projects/{status_id}', response_model=FindProjectbyStatusReponse, responses=generate_error_responses())
async def find_project_by_status(status_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['status_id'] = status_id
        http_response = await request_adapter(request, find_project_by_status_composer())
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