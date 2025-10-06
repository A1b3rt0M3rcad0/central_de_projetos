from fastapi import APIRouter, Request, Security
from src.main.routes.api.notification.notification_response.find_notifications_response import FindNotificationsResponse
from src.main.routes.api.notification.notification_response.mark_notification_as_read_response import MarkNotificationAsReadResponse
from src.main.routes.api.notification.notification_response.count_unread_notifications_response import CountUnreadNotificationsResponse
from src.main.routes.middleware.authorization import role_required
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler
from src.main.composers.find_notifications_composer import find_notifications_composer
from src.main.composers.mark_notification_as_read_composer import mark_notification_as_read_composer
from src.main.composers.count_unread_notifications_composer import count_unread_notifications_composer
from src.logs.log_http import log_http
from src.main.routes.api.__error.error_response import generate_error_responses

PREFIX = '/notification'
TAGS = ['notification']
routes = APIRouter(prefix=PREFIX, tags=TAGS)


@routes.get('/find', response_model=FindNotificationsResponse, responses=generate_error_responses())
async def find_notifications(
    request: Request,
    recipient_cpf: str,
    limit: int = 20,
    offset: int = 0,
    unread_only: bool = False,
    user: dict = Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))  # pylint: disable=unused-argument
):
    """
    Endpoint para buscar notificações de um usuário.
    
    Args:
        request: Objeto da requisição HTTP
        recipient_cpf: CPF do destinatário das notificações
        limit: Limite de resultados (padrão: 20)
        offset: Offset para paginação (padrão: 0)
        unread_only: Se deve retornar apenas não lidas (padrão: False)
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindNotificationsResponse: Lista de notificações
        
    Raises:
        UnauthorizedError: Se o usuário não estiver autenticado
        InternalServerError: Para outros erros internos
    """
    try:
        # Criar um novo request com os parâmetros
        from src.presentation.http_types.http_request import HttpRequest
        http_request = HttpRequest(
            body={},
            headers=dict(request.headers),
            query_params={
                'recipient_cpf': recipient_cpf,
                'limit': limit,
                'offset': offset,
                'unread_only': unread_only
            },
            path_params=request.path_params,
            url=str(request.url)
        )
        
        # Processar requisição
        http_response = find_notifications_composer()(http_request)
        
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        
        return response_adapter(http_response)
        
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)


@routes.post('/mark_as_read', response_model=MarkNotificationAsReadResponse, responses=generate_error_responses())
async def mark_notification_as_read(
    request: Request,
    user: dict = Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))  # pylint: disable=unused-argument
):
    """
    Endpoint para marcar uma notificação como lida.
    
    Args:
        request: Objeto da requisição HTTP (deve conter notification_id como query parameter)
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Query Parameters:
        notification_id: ID da notificação a ser marcada como lida
        
    Returns:
        MarkNotificationAsReadResponse: Confirmação da operação
        
    Raises:
        UnauthorizedError: Se o usuário não estiver autenticado
        NotificationNotFoundError: Se a notificação não for encontrada
        InternalServerError: Para outros erros internos
    """
    try:
        # Extrair notification_id dos query parameters
        notification_id = request.query_params.get('notification_id')
        
        if not notification_id:
            from src.presentation.http_types.http_response import HttpResponse
            return HttpResponse(
                status_code=400,
                body={'error': 'notification_id é obrigatório'}
            )
        
        # Criar um novo request com os dados
        from src.presentation.http_types.http_request import HttpRequest
        http_request = HttpRequest(
            body={
                'notification_id': int(notification_id)
            },
            headers=dict(request.headers),
            query_params=dict(request.query_params),
            path_params=request.path_params,
            url=str(request.url)
        )
        
        # Processar requisição
        http_response = mark_notification_as_read_composer()(http_request)
        
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        
        return response_adapter(http_response)
        
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)


@routes.get('/count_unread', response_model=CountUnreadNotificationsResponse, responses=generate_error_responses())
async def count_unread_notifications(
    request: Request,
    recipient_cpf: str,
    user: dict = Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))  # pylint: disable=unused-argument
):
    """
    Endpoint para contar notificações não lidas de um usuário.
    
    Args:
        request: Objeto da requisição HTTP
        recipient_cpf: CPF do destinatário das notificações
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        CountUnreadNotificationsResponse: Número de notificações não lidas
        
    Raises:
        UnauthorizedError: Se o usuário não estiver autenticado
        InternalServerError: Para outros erros internos
    """
    try:
        # Criar um novo request com os parâmetros
        from src.presentation.http_types.http_request import HttpRequest
        http_request = HttpRequest(
            body={},
            headers=dict(request.headers),
            query_params={
                'recipient_cpf': recipient_cpf
            },
            path_params=request.path_params,
            url=str(request.url)
        )
        
        # Processar requisição
        http_response = count_unread_notifications_composer()(http_request)
        
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        
        return response_adapter(http_response)
        
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)
