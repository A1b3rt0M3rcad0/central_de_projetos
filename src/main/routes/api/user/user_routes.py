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
from src.main.composers.who_am_i_composer import who_am_i_composer
from src.main.composers.find_all_user_composer import find_all_user_composer
from src.main.composers.find_all_user_by_role_composer import find_all_user_by_role_composer

from src.main.routes.api.user.request_format.create_user_format import CreateUserFormat
from src.main.routes.api.user.request_format.delete_user_format import DeleteUserFormat
from src.main.routes.api.user.request_format.update_user_email_format import UpdateUserEmailFormat
from src.main.routes.api.user.request_format.update_user_password_format import UpdateUserPasswordFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.user.user_response.get_user_response import GetUserResponse
from src.main.routes.api.user.user_response.get_all_users_response import GetAllUsersResponse
from src.main.routes.api.user.user_response.get_all_users_by_role import GetAllUsersByRoleResponse
from src.main.routes.api.user.user_response.who_am_i_response import WhoAmIReponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/users'
TAGS = ['users']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get("/{user_cpf}", response_model=GetUserResponse, responses=generate_error_responses())
async def get_user(user_cpf: str, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar um usuário específico pelo CPF.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        user_cpf: CPF do usuário a ser buscado
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        GetUserResponse: Dados do usuário encontrado
        
    Raises:
        UserNotFoundError: Se o usuário não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, find_user_composer())
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
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.get("/users/all", response_model=GetAllUsersResponse, responses=generate_error_responses())
async def get_all_users(request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os usuários do sistema.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        GetAllUsersResponse: Lista com todos os usuários do sistema
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, find_all_user_composer())
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
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.get("/users/all/{role}", response_model=GetAllUsersByRoleResponse, responses=generate_error_responses())
async def get_all_users_by_role(role:str, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os usuários filtrados por role (papel).
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        role: Role/papel dos usuários a serem buscados (ADMIN, VEREADOR, ASSESSOR)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        GetAllUsersByRoleResponse: Lista de usuários com o role especificado
        
    Raises:
        InvalidRoleError: Se o role fornecido for inválido
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params["role"] = role
        http_response = await request_adapter(request, find_all_user_by_role_composer())
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
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.get("/who_am_i/{token}", response_model=WhoAmIReponse, responses=generate_error_responses())
async def who_am_i(token: str, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para obter informações do usuário autenticado através do token JWT.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        token: Token JWT do usuário
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        WhoAmIResponse: Dados do usuário autenticado
        
    Raises:
        InvalidTokenError: Se o token for inválido ou expirado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, who_am_i_composer())
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
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.post("/", response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_user(body:CreateUserFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar um novo usuário no sistema.
    Apenas usuários ADMIN podem criar novos usuários.
    
    Args:
        body: Dados do usuário a ser criado (CPF, nome, email, senha, role)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        UserAlreadyExistsError: Se o usuário já existir (CPF ou email duplicado)
        InvalidCPFError: Se o CPF for inválido
        InvalidEmailError: Se o email for inválido
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, create_user_composer())
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
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.delete("/", response_model=BaseMessageResponse, responses=generate_error_responses())
async def delete_user(body:DeleteUserFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar um usuário do sistema.
    Apenas usuários ADMIN podem deletar usuários.
    
    Args:
        body: Dados do usuário a ser deletado (CPF)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        UserNotFoundError: Se o usuário não for encontrado
        UserHasRelatedChildrenError: Se o usuário possui relacionamentos que impedem a deleção
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_user_composer())
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
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.patch("/password", response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_password(body:UpdateUserPasswordFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para atualizar a senha de um usuário.
    Apenas usuários ADMIN podem alterar senhas.
    
    Args:
        body: Dados para atualização (CPF do usuário e nova senha)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na atualização
        
    Raises:
        UserNotFoundError: Se o usuário não for encontrado
        InvalidPasswordError: Se a nova senha não atender aos critérios
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, update_user_password_composer())
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
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.patch("/email", response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_email(body:UpdateUserEmailFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para atualizar o email de um usuário.
    Apenas usuários ADMIN podem alterar emails.
    
    Args:
        body: Dados para atualização (CPF do usuário e novo email)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na atualização
        
    Raises:
        UserNotFoundError: Se o usuário não for encontrado
        InvalidEmailError: Se o novo email for inválido
        EmailAlreadyExistsError: Se o email já estiver em uso
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, update_user_email_composer())
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
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)