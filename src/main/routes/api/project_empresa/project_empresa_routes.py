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

from src.main.routes.api.project_empresa.request_format.create_project_empresa_format import CreateProjectEmpresaFormat
from src.main.routes.api.project_empresa.request_format.delete_project_empresa_format import DeleteProjectEmpresaFormat

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

routes = APIRouter(prefix='/project_empresa', tags=['project', 'empresa', 'project_empresa'])

@routes.get('/{empresa_id}/{project_id}')
async def find_project_empresa(empresa_id:int, project_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['empresa_id'] = empresa_id
        request.path_params['project_id'] = project_id
        http_response = await request_adapter(request, find_project_empresa_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.get('/{empresa_id}')
async def find_all_projects_from_empresa(empresa_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['empresa_id'] = empresa_id
        http_response = request_adapter(request, find_all_projects_from_empresa_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post('/')
async def create_project_empresa(body:CreateProjectEmpresaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_project_empresa_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete('/')
async def delete_project_empresa(body:DeleteProjectEmpresaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_project_empresa_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))