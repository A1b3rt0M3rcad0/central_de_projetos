#pylint:disable=W0718
#pylint:disable=W0613
#pylint:disable=all
from io import BytesIO
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_type_composer import create_type_composer
from src.main.composers.delete_type_composer import delete_type_composer
from src.main.composers.find_type_by_exact_name_composer import find_type_by_exact_name_composer
from src.main.composers.update_type_composer import update_type_composer
from src.main.composers.find_all_types_composer import find_all_types_composer

from src.main.routes.api.types.request_format.create_type_format import CreateTypeFormat
from src.main.routes.api.types.request_format.delete_type_format import DeleteTypeFormat
from src.main.routes.api.types.request_format.update_type_format import UpdateTypeFormat

routes = APIRouter(prefix='/types', tags=['type'])

@routes.post('/')
async def create_type(body:CreateTypeFormat, request:Request):
    try:
        http_response = await request_adapter(request, create_type_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete('/')
async def delete_type(body:DeleteTypeFormat, request:Request):
    try:
        http_response = await request_adapter(request, delete_type_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/')
async def update_type(body:UpdateTypeFormat, request:Request):
    try:
        http_response = await request_adapter(request, update_type_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.get('/find_by_name/{type_name}')
async def find_type_by_exact_name(type_name:str, request:Request):
    try:
        request.path_params['type_name'] = type_name
        http_response = await request_adapter(request, find_type_by_exact_name_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.get('/all')
async def find_all_types(request:Request):
    try:
        http_response = await request_adapter(request, find_all_types_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))