#pylint:disable=all
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.validator_handle.validator_handle import validator_handler
from src.errors.error_handle import error_handler
from src.main.composers.find_user_composer import find_user_composer
from src.main.composers.create_user_composer import create_user_composer
from src.main.composers.delete_user_composer import delete_user_composer
from src.main.composers.update_user_email_composer import update_user_email_composer
from src.main.composers.update_user_password_composer import update_user_password_composer

from src.main.routes.user.request_format.find_user_format import FindUserFormat
from src.main.routes.user.request_format.create_user_format import CreateUserFormat
from src.main.routes.user.request_format.delete_user_format import DeleteUserFormat
from src.main.routes.user.request_format.update_user_email_format import UpdateUserEmailFormat
from src.main.routes.user.request_format.update_user_password_format import UpdateUserPasswordFormat

routes = APIRouter(prefix='/users', tags=['users'])

@routes.get("/{user_cpf}")
async def get_user(user_cpf: str, request: Request):
    try:
        request.path_params['user_cpf'] = user_cpf

        validator_handler(FindUserFormat, {'user_cpf': user_cpf})
        
        http_response = await request_adapter(request, find_user_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.post("/")
async def create_user(request:Request):
    try:

        body = await request.json()

        validator_handler(CreateUserFormat, body)

        http_response = await request_adapter(request, create_user_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.delete("/")
async def delete_user(request:Request):
    try:

        body = await request.json()

        validator_handler(DeleteUserFormat, body)

        http_response = await request_adapter(request, delete_user_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch("/password")
async def update_password(request:Request):
    try:

        body = await request.json()

        validator_handler(UpdateUserPasswordFormat, body)

        http_response = await request_adapter(request, update_user_password_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))

@routes.patch("/email")
async def update_email(request:Request):
    try:

        body = await request.json()

        validator_handler(UpdateUserEmailFormat, body)

        http_response = await request_adapter(request, update_user_email_composer())
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))