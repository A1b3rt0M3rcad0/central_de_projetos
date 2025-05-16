#pylint:disable=W0718
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.validator_handle.validator_handle import validator_handler
from src.errors.error_handle import error_handler

from src.main.composers.find_bairro_by_name_composer import find_bairro_by_name_composer
from src.main.composers.create_bairro_composer import create_bairro_composer
from src.main.composers.delete_bairro_composer import delete_bairro_composer
from src.main.composers.update_bairro_name_composer import update_bairro_name_composer


from src.main.routes.api.bairro.request_format.find_bairro_by_name_format import FindBairroByNameFormat
from src.main.routes.api.bairro.request_format.create_bairro_format import CreateBairroFormat
from src.main.routes.api.bairro.request_format.delete_bairro_format import DeleteBairroFormat
from src.main.routes.api.bairro.request_format.update_bairro_name_format import UpdateBairroNameFormat

routes = APIRouter(prefix='/bairro', tags=['bairros'])

@routes.get('/{bairro_name}')
async def find_bairro_by_name(bairro_name:str, request:Request):
    try:
        request.path_params['bairro_name'] = bairro_name

        validator_handler(FindBairroByNameFormat, {'bairro_name': bairro_name})

        http_response = await request_adapter(request, find_bairro_by_name_composer())
        return response_adapter(http_response)

    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post('/')
async def create_bairro(request:Request):
    try:

        body = await request.json()

        validator_handler(CreateBairroFormat, body)

        http_response = await request_adapter(request, create_bairro_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete('/')
async def delete_bairro(request:Request):
    try:

        body = await request.json()

        validator_handler(DeleteBairroFormat, body)

        http_response = await request_adapter(request, delete_bairro_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/name')
async def update_bairro_name(request:Request):
    try:
        body = await request.json()

        validator_handler(UpdateBairroNameFormat, body)

        http_response = await request_adapter(request, update_bairro_name_composer())
        return response_adapter(http_response) 
    except Exception as e:
        return response_adapter(error_handler(e))