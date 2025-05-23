#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_project_composer import find_project_composer
from src.main.composers.delete_project_composer import delete_project_composer
from src.main.composers.create_project_composer import create_project_composer
from src.main.composers.update_project_name_composer import update_project_name_composer
from src.main.composers.update_project_andamento_composer import update_project_andamento_composer
from src.main.composers.update_project_end_date_composer import update_project_end_date_composer
from src.main.composers.update_project_expected_completion_date_composer import update_projet_expected_completion_date_composer
from src.main.composers.update_project_start_date_composer import update_project_start_date_composer
from src.main.composers.update_project_verba_composer import update_project_verba_composer

from src.main.routes.api.project.request_format.create_project_format import CreateProjectFormat
from src.main.routes.api.project.request_format.update_project_name_format import UpdateProjectNameFormat
from src.main.routes.api.project.request_format.delete_project_format import DeleteProjectFormat
from src.main.routes.api.project.request_format.update_project_andamento_format import UpdateProjectAndamentoFormat
from src.main.routes.api.project.request_format.update_end_date_project_format import UpdateEndDateProjectFormat
from src.main.routes.api.project.request_format.update_expected_completion_date_format import UpdateExpectedCompletionDateFormat
from src.main.routes.api.project.request_format.update_start_date_format import UpdateStartDateFormat
from src.main.routes.api.project.request_format.update_verba_format import UpdateVerbaFormat

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

routes = APIRouter(prefix='/project', tags=['project'])

@routes.get('/{project_id}')
async def find_project(project_id, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['project_id'] = project_id
        http_response = await request_adapter(request, find_project_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post('/')
async def create_project(body:CreateProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_project_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete('/')
async def delete_project(body:DeleteProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_project_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/name')
async def update_project_name(body:UpdateProjectNameFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/andamento_do_projeto')
async def update_project_andamento(body:UpdateProjectAndamentoFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_andamento_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/end_date')
async def update_end_date(body:UpdateEndDateProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_end_date_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/projet_expected_completion_date')
async def update_expected_completion_date(body:UpdateExpectedCompletionDateFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_projet_expected_completion_date_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/start_date')
async def update_start_date(body:UpdateStartDateFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_start_date_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/verba')
async def update_project_verba(body:UpdateVerbaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_project_verba_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))