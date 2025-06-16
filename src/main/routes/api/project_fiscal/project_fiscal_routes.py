#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

## Composers
from src.main.composers.create_project_fiscal_composer import create_project_fiscal_composer
from src.main.composers.delete_project_fiscal_composer import delete_project_fiscal_composer

## request Formats
from src.main.routes.api.project_fiscal.request_format.create_project_fiscal import CreateProjectFiscalFormat
from src.main.routes.api.project_fiscal.request_format.delete_project_fiscal import DeleteProjectFiscalFormat

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

routes = APIRouter(prefix='/project_fiscal', tags=['project', 'fiscal', 'project_fiscal'])

@routes.post("/")
async def create_project_fiscal(body:CreateProjectFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_project_fiscal_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete("/")
async def delete_project_fiscal(body:DeleteProjectFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_project_fiscal_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))