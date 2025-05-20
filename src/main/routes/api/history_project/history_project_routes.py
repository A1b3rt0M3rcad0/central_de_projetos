#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_history_project_composer import create_history_project_composer
from src.main.composers.find_all_history_from_project_composer import find_all_history_from_project_composer

from src.main.routes.api.history_project.request_format.create_history_project_format import CreateHistoryProjectFormat
from src.main.routes.api.history_project.request_format.find_all_hisotry_from_project_format import FindAllHistoryFromProjectFormat

routes = APIRouter(prefix='/history_project', tags=['history_project', 'project'])

@routes.get('/')
async def find_all_history_from_project(body:FindAllHistoryFromProjectFormat, request:Request):
    try:
        http_response = await request_adapter(request, find_all_history_from_project_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post('/')
async def create_history_project(body:CreateHistoryProjectFormat, request:Request):
    try:
        http_response = await request_adapter(request, create_history_project_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))