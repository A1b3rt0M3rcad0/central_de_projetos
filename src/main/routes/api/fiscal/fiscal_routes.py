#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_fiscal_by_name_composer import find_fiscal_by_name_composer
from src.main.composers.create_fiscal_composer import create_fiscal_composer
from src.main.composers.delete_fiscal_composer import delete_fiscal_composer
from src.main.composers.update_fiscal_name_composer import update_fiscal_name_composer
from src.main.composers.find_all_fiscal_composer import find_all_fiscal_composer

from src.main.routes.api.fiscal.request_format.create_fiscal_format import CreateFiscalFormat
from src.main.routes.api.fiscal.request_format.delete_fiscal_format import DeleteFiscalFormat
from src.main.routes.api.fiscal.request_format.update_fiscal_name_format import UpdateFiscalNameFormat

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

routes = APIRouter(prefix='/fiscal', tags=['fiscal'])

@routes.get('/{fiscal_name}')
async def find_fiscal_by_name(fiscal_name, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        request.path_params['fiscal_name'] = fiscal_name
        http_response = await request_adapter(request, find_fiscal_by_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.get('/fiscal/all')
async def find_all_fiscal(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_fiscal_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post('/')
async def create_fiscal(body:CreateFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_fiscal_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete('/')
async def delete_fiscal(body:DeleteFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_fiscal_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/')
async def update_fiscal(body:UpdateFiscalNameFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_fiscal_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))