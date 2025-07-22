#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.update_association_from_project_composer import update_association_from_project_composer
from src.main.composers.delete_association_composer import delete_association_composer
from src.main.composers.find_all_association_from_projects_composer import find_all_association_from_projects_composer
from src.main.composers.associate_vereador_with_a_project_composer import associate_vereador_with_a_project_composer
from src.main.composers.get_count_projects_by_user_composer import get_count_projets_by_user_composer

from src.main.routes.api.user_project.request_format.associate_vereador_with_a_project_format import AssociateVereadorWithAProjectFormat
from src.main.routes.api.user_project.request_format.delete_association_format import DeleteAssociationFormat
from src.main.routes.api.user_project.request_format.update_association_from_project_format import UpdateAssociationFromProjectFormat

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/user_project'
TAGS = ['user', 'project', 'user_project']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/all')
async def find_all_association_from_projects(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_association_from_projects_composer())
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

@routes.get('/project/count/all')
async def get_count_projets_by_user(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, get_count_projets_by_user_composer())
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

@routes.post('/')
async def associate_vereador_with_a_project(body:AssociateVereadorWithAProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, associate_vereador_with_a_project_composer())
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
async def delete_association(body:DeleteAssociationFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_association_composer())
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

@routes.patch('/')
async def update_association_from_project(body:UpdateAssociationFromProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_association_from_project_composer())
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