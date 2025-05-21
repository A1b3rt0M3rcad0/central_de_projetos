#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_project_type_composer import create_project_type_composer
from src.main.composers.find_type_from_project_composer import find_type_from_project_composer
from src.main.composers.delete_project_type_composer import delete_project_type_composer

from src.main.routes.api.project_type.request_format.create_project_type_format import CreateProjectTypeFormat
from src.main.routes.api.project_type.request_format.delete_project_type_format import DeleteProjectTypeFormat

routes = APIRouter(prefix='/project_type', tags=['project', 'type'])

@routes.get('/{project_id}')
async def find_type_from_project(project_id:int, request:Request):
    try:
        request.path_params['project_id'] = project_id
        http_response = await request_adapter(request, find_type_from_project_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post('/')
async def create_project_type(body:CreateProjectTypeFormat, request:Request):
    try:
        http_response  = await request_adapter(request, create_project_type_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))
    
@routes.delete('/')
async def delete_project_type(body:DeleteProjectTypeFormat, request:Request):
    try:
        http_response = await request_adapter(request, delete_project_type_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))