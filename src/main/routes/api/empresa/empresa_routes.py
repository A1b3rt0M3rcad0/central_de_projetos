#pylint:disable=W0718
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.validator_handle.validator_handle import validator_handler
from src.errors.error_handle import error_handler

from src.main.composers.find_empresa_by_exact_name_composer import find_empresa_by_exact_name_composer
from src.main.composers.create_empresa_composer import create_empresa_composer
from src.main.composers.delete_empresa_composer import delete_empresa_composer
from src.main.composers.update_empresa_composer import update_empresas_composer

from src.main.routes.api.empresa.request_format.create_empresa_format import CreateEmpresaFormat
from src.main.routes.api.empresa.request_format.delete_empresa_format import DeleteEmpresaFormat
from src.main.routes.api.empresa.request_format.find_empresa_by_exact_name_format import FindEmpresaByExactNameFormat
from src.main.routes.api.empresa.request_format.update_empresas_composer import UpdateEmpresasFormat

routes = APIRouter(prefix='/empresa', tags=['empresas'])

@routes.get('/{empresa_name}')
async def find_empresa(empresa_name, request:Request):
    try:
        request.path_params['empresa_name'] = empresa_name
        validator_handler(FindEmpresaByExactNameFormat, {'empresa_name':empresa_name})
        http_response = await request_adapter(request, find_empresa_by_exact_name_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post('/')
async def create_empresa(request:Request):
    try:
        body = await request.json()
        validator_handler(CreateEmpresaFormat, body)
        http_response = await request_adapter(request, create_empresa_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete('/')
async def delete_empresa(request:Request):
    try:
        body = await request.json()
        validator_handler(DeleteEmpresaFormat, body)
        http_response = await request_adapter(request, delete_empresa_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch('/')
async def update_empresa(request:Request):
    try:
        body = await request.json()
        validator_handler(UpdateEmpresasFormat, body)
        http_response = await request_adapter(request, update_empresas_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))