#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_project_composer import find_project_composer
from src.main.composers.find_all_projects_composer import find_all_projects_composer
from src.main.composers.delete_project_composer import delete_project_composer
from src.main.composers.create_project_composer import create_project_composer
from src.main.composers.update_project_name_composer import update_project_name_composer
from src.main.composers.update_project_andamento_composer import update_project_andamento_composer
from src.main.composers.update_project_end_date_composer import update_project_end_date_composer
from src.main.composers.update_project_expected_completion_date_composer import update_projet_expected_completion_date_composer
from src.main.composers.update_project_start_date_composer import update_project_start_date_composer
from src.main.composers.update_project_verba_composer import update_project_verba_composer
from src.main.composers.find_all_from_project_composer import find_all_from_project_composer
from src.main.composers.find_all_projects_with_basic_details_composer import find_all_projects_with_basic_details_composer
from src.main.composers.update_status_from_project_composer import update_status_from_project_composer
from src.main.composers.find_all_associations_possibility_from_project_composer import find_all_associations_possibility_from_project_composer
from src.main.composers.count_projects_composer import count_projects_composer
from src.main.composers.get_projects_with_pagination_composer import get_projects_with_pagination_composer

from src.main.routes.api.project.request_format.create_project_format import CreateProjectFormat
from src.main.routes.api.project.request_format.update_project_name_format import UpdateProjectNameFormat
from src.main.routes.api.project.request_format.delete_project_format import DeleteProjectFormat
from src.main.routes.api.project.request_format.update_project_andamento_format import UpdateProjectAndamentoFormat
from src.main.routes.api.project.request_format.update_end_date_project_format import UpdateEndDateProjectFormat
from src.main.routes.api.project.request_format.update_expected_completion_date_format import UpdateExpectedCompletionDateFormat
from src.main.routes.api.project.request_format.update_start_date_format import UpdateStartDateFormat
from src.main.routes.api.project.request_format.update_verba_format import UpdateVerbaFormat
from src.main.routes.api.project.request_format.update_status_format import UpdateStartStatusFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.project.project_response.find_project_response import FindProjectResponse
from src.main.routes.api.project.project_response.count_project_response import CountProjectResponse
from src.main.routes.api.project.project_response.find_all_projects_response import FindAllProjectsResponse
from src.main.routes.api.project.project_response.find_associations_projects_response import FindAssociationProjectsResponse
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.project.project_response.find_all_projects_with_basic_details_response import FindAllProjectWithBasicDetailsResponse
from src.main.routes.api.project.project_response.project_detail_response import ProjectDetailResponse
from src.main.routes.api.project.project_response.get_projects_with_pagination_response import GetProjectsWithPaginationReponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logger
from src.logs.log_http import log_http

PREFIX =  '/project'
TAGS = ['project']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{project_id}', response_model=FindProjectResponse, responses=generate_error_responses())
async def find_project(project_id, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['project_id'] = project_id
        http_response = await request_adapter(request, find_project_composer())
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

@routes.get('/count/all', response_model=CountProjectResponse, responses=generate_error_responses())
async def count_projects(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, count_projects_composer())
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

@routes.get('/projects/all', response_model=FindAllProjectsResponse, responses=generate_error_responses(), deprecated=True)
async def find_all_projects(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_projects_composer())
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

@routes.get('/projects/associations/all', response_model=FindAssociationProjectsResponse, responses=generate_error_responses())
async def find_associations_projects(request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, find_all_associations_possibility_from_project_composer())
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

@routes.get('/projects/all/details', response_model=FindAllProjectWithBasicDetailsResponse, responses=generate_error_responses())
async def find_all_projects_details(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_projects_with_basic_details_composer())
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
async def create_project(body:CreateProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_project_composer())
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
async def delete_project(body:DeleteProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_project_composer())
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

@routes.patch('/name', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_project_name(body:UpdateProjectNameFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_name_composer())
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

@routes.patch('/andamento_do_projeto', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_project_andamento(body:UpdateProjectAndamentoFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_andamento_composer())
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

@routes.patch('/end_date', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_end_date(body:UpdateEndDateProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_end_date_composer())
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

@routes.patch('/projet_expected_completion_date', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_expected_completion_date(body:UpdateExpectedCompletionDateFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_projet_expected_completion_date_composer())
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

@routes.patch('/start_date', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_start_date(body:UpdateStartDateFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_start_date_composer())
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

@routes.patch('/verba', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_project_verba(body:UpdateVerbaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_verba_composer())
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

@routes.patch('/status', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_project_status(body:UpdateStartStatusFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_status_from_project_composer())
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

@routes.get('/project_detail/{project_id}', response_model=ProjectDetailResponse, responses=generate_error_responses())
async def project_detail(project_id, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['project_id'] = project_id
        http_response = await request_adapter(request, find_all_from_project_composer())
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

@routes.get('/projects/pagination/{page_size}/{page}', response_model=GetProjectsWithPaginationReponse, responses=generate_error_responses())
async def get_projects_with_pagination(page_size:int, page:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, get_projects_with_pagination_composer())
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