#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.login_composer import login_composer

from src.main.routes.api.auth.request_format.login_format import LoginFormat

#Limiter
from src.main.routes.middleware.rate_limit import limiter

# Logger
from src.logs.log_http import log_http

routes = APIRouter(prefix='/auth', tags=['auth', 'login'])

@routes.post('/login')
@limiter.limit("5/minute")
async def login(body:LoginFormat, request:Request):
    try:
        http_response = await request_adapter(request, login_composer())
        response = response_adapter(http_response)
        # response.set_cookie('access_token', value=http_response.body.get('token'), httponly=False, secure=False)
        log_http(
            logger_name='/auth',
            level="INFO",
            http_response=http_response
        )
        return response
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            logger_name='/auth',
            level="ERROR",
            http_response=error_result
        )
        return response_adapter(error_result)