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

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

routes = APIRouter(prefix='/status', tags=['status'])

@routes.get('/{status_id}')
async def find_status(status_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['status_id'] = status_id
        http_response = await request_adapter(request, find_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post('/')
async def create_status(body:CreateStatusFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete('/')
async def delete_status(body:DeleteStatusFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/')
async def update_status_description(body:UpdateStatusDescriptionFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_status_description_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))
    
@routes.get('/all/')
async def find_all_status(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.get('/projects/{status_id}')
async def find_project_by_status(status_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['status_id'] = status_id
        http_response = await request_adapter(request, find_project_by_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))