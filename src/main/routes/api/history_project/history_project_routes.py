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

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/history_project'
TAGS = ['history_project', 'project']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/')
async def find_all_history_from_project(body:FindAllHistoryFromProjectFormat, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_all_history_from_project_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(error_result)

@routes.post('/')
async def create_history_project(body:CreateHistoryProjectFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_history_project_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(error_result)