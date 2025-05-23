#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler
from src.main.composers.find_user_composer import find_user_composer
from src.main.composers.create_user_composer import create_user_composer
from src.main.composers.delete_user_composer import delete_user_composer
from src.main.composers.update_user_email_composer import update_user_email_composer
from src.main.composers.update_user_password_composer import update_user_password_composer

from src.main.routes.api.user.request_format.create_user_format import CreateUserFormat
from src.main.routes.api.user.request_format.delete_user_format import DeleteUserFormat
from src.main.routes.api.user.request_format.update_user_email_format import UpdateUserEmailFormat
from src.main.routes.api.user.request_format.update_user_password_format import UpdateUserPasswordFormat

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

routes = APIRouter(prefix='/users', tags=['users'])

@routes.get("/{user_cpf}")
async def get_user(user_cpf: str, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    try:
        http_response = await request_adapter(request, find_user_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post("/")
async def create_user(body:CreateUserFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, create_user_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete("/")
async def delete_user(body:DeleteUserFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, delete_user_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch("/password")
async def update_password(body:UpdateUserPasswordFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_user_password_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch("/email")
async def update_email(body:UpdateUserEmailFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    try:
        http_response = await request_adapter(request, update_user_email_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))