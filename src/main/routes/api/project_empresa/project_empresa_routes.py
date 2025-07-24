#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_project_empresa_composer import create_project_empresa_composer
from src.main.composers.delete_project_empresa_composer import delete_project_empresa_composer
from src.main.composers.find_project_empresa_composer import find_project_empresa_composer
from src.main.composers.find_all_projects_from_empresa_composer import find_all_projects_from_empresa_composer
from src.main.composers.get_count_projects_by_empresas_composer import get_count_projects_by_empresas_composer

from src.main.routes.api.project_empresa.request_format.create_project_empresa_format import CreateProjectEmpresaFormat
from src.main.routes.api.project_empresa.request_format.delete_project_empresa_format import DeleteProjectEmpresaFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.project_empresa.project_empresa_response.find_project_empresa_response import FindProjectEmpresaResponse
from src.main.routes.api.project_empresa.project_empresa_response.find_all_projects_from_empresa_response import FindAllProjectsFromEmpresaResponse
from src.main.routes.api.project_empresa.project_empresa_response.get_count_projects_by_empresa_response import GetCountProjectsByEmpresaResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/project_empresa'
TAGS = ['project', 'empresa', 'project_empresa']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{empresa_id}/{project_id}', response_model=FindProjectEmpresaResponse, responses=generate_error_responses())
async def find_project_empresa(empresa_id:int, project_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['empresa_id'] = empresa_id
        request.path_params['project_id'] = project_id
        http_response = await request_adapter(request, find_project_empresa_composer())
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

@routes.get('/{empresa_id}', response_model=FindAllProjectsFromEmpresaResponse, responses=generate_error_responses())
async def find_all_projects_from_empresa(empresa_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['empresa_id'] = empresa_id
        http_response = await request_adapter(request, find_all_projects_from_empresa_composer())
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

@routes.get('/project/count/all', response_model=GetCountProjectsByEmpresaResponse, responses=generate_error_responses())
async def get_count_projects_by_empresas(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, get_count_projects_by_empresas_composer())
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
async def create_project_empresa(body:CreateProjectEmpresaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_project_empresa_composer())
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
async def delete_project_empresa(body:DeleteProjectEmpresaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_project_empresa_composer())
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