#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.login_composer import login_composer

from src.main.routes.api.auth.request_format.login_format import LoginFormat

routes = APIRouter(prefix='/auth', tags=['auth', 'login'])

@routes.post('/login')
async def login(body:LoginFormat, request:Request):
    try:
        http_response = await request_adapter(request, login_composer())
        response = response_adapter(http_response)
        response.set_cookie('acess_token', value=http_response.body.get('token'), httponly=True, secure=True)
        return response
    except Exception as e:
        return response_adapter(error_handler(e))