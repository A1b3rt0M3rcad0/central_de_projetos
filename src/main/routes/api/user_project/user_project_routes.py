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

from src.main.routes.api.user_project.request_format.associate_vereador_with_a_project_format import AssociateVereadorWithAProjectFormat
from src.main.routes.api.user_project.request_format.delete_association_format import DeleteAssociationFormat
from src.main.routes.api.user_project.request_format.update_association_from_project_format import UpdateAssociationFromProjectFormat

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

routes = APIRouter(prefix='/user_project', tags=['user', 'project', 'user_project'])

@routes.get('/all')
async def find_all_association_from_projects(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_association_from_projects_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post('/')
async def associate_vereador_with_a_project(body:AssociateVereadorWithAProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, associate_vereador_with_a_project_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete('/')
async def delete_association(body:DeleteAssociationFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_association_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/')
async def update_association_from_project(body:UpdateAssociationFromProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_association_from_project_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))