#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_project_bairro_composer import find_project_bairro_composer
from src.main.composers.create_project_bairro_composer import create_project_bairro_composer
from src.main.composers.delete_project_bairro_composer import delete_project_bairro_composer
from src.main.composers.find_all_projects_from_bairro_composer import find_all_projects_from_bairro_composer
from src.main.composers.get_project_counts_by_bairro_composer import get_project_counts_by_bairro_composer
from src.main.composers.get_project_verba_by_bairro_composer import get_project_verba_by_bairro
from src.main.composers.get_project_status_count_by_bairro_composer import get_project_status_count_by_bairro_composer

from src.main.routes.api.project_bairro.request_format.create_project_bairro_format import CreateProjectBairroFormat
from src.main.routes.api.project_bairro.request_format.delete_project_bairro_format import DeleteProjectBairroFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.project_bairro.project_bairro_response.find_project_bairro_response import FindProjectBairroResponse
from src.main.routes.api.project_bairro.project_bairro_response.get_project_counts_by_bairro_response import GetProjectCountByBairroResponse
from src.main.routes.api.project_bairro.project_bairro_response.get_project_verba_by_bairro_response import GetProjectVerbaByBairroResponse
from src.main.routes.api.project_bairro.project_bairro_response.get_project_status_count_by_bairro_response import GetProjectStatusCountByBairroResponse
from src.main.routes.api.project_bairro.project_bairro_response.find_all_projects_from_bairro_response import FindAllProjectsFromBairroResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/project_bairro'
TAGS = ['project', 'bairro']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{bairro_id}/{project_id}', response_model=FindProjectBairroResponse, responses=generate_error_responses())
async def find_project_bairro(bairro_id:int, project_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['project_id'] = project_id
        request.path_params['bairro_id'] = bairro_id
        http_response = await request_adapter(request, find_project_bairro_composer())
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

@routes.get('/project/count/', response_model=GetProjectCountByBairroResponse, responses=generate_error_responses())
async def get_project_counts_by_bairro(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, get_project_counts_by_bairro_composer())
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

@routes.get('/project/verba/', response_model=GetProjectVerbaByBairroResponse, responses=generate_error_responses())
async def get_project_verba_by_bairro_r(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, get_project_verba_by_bairro())
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

@routes.get('/project/status/', response_model=GetProjectStatusCountByBairroResponse, responses=generate_error_responses())
async def get_project_status_count_by_bairro_r(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, get_project_status_count_by_bairro_composer())
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
async def create_project_bairro(body:CreateProjectBairroFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_project_bairro_composer())
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
async def delete_project_bairro(body:DeleteProjectBairroFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_project_bairro_composer())
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

@routes.get('/{bairro_id}', response_model=FindAllProjectsFromBairroResponse, responses=generate_error_responses())
async def find_all_projects_from_bairro(bairro_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['bairro_id'] = bairro_id
        http_response = await request_adapter(request, find_all_projects_from_bairro_composer())
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