from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_find_notifications import IFindNotifications


class FindNotificationsController(ControllerInterface):
    """Controller para buscar notificações"""

    def __init__(self, find_notifications_case: IFindNotifications) -> None:
        self.__find_notifications_case = find_notifications_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """Handle para buscar notificações"""
        try:
            # Extrair dados da requisição (query params)
            recipient_cpf = http_request.query_params.get('recipient_cpf')
            limit = http_request.query_params.get('limit')
            offset = http_request.query_params.get('offset')
            unread_only = http_request.query_params.get('unread_only', False)
            
            # Converter tipos se necessário
            if limit:
                limit = int(limit)
            if offset:
                offset = int(offset)
            if isinstance(unread_only, str):
                unread_only = unread_only.lower() == 'true'
            
            if not recipient_cpf:
                return HttpResponse(
                    status_code=400,
                    body={'error': 'recipient_cpf é obrigatório'}
                )
            
            # Buscar notificações
            notifications = self.__find_notifications_case.find_by_recipient(
                recipient_cpf=recipient_cpf,
                limit=limit,
                offset=offset,
                unread_only=unread_only
            )
            
            # Converter entidades para dicionários
            notifications_data = []
            for notification in notifications:
                notifications_data.append({
                    'notification_id': notification.notification_id,
                    'recipient_cpf': notification.recipient_cpf,
                    'notification_type': notification.notification_type.value,
                    'title': notification.title,
                    'message': notification.message,
                    'is_read': notification.is_read,
                    'read_at': notification.read_at.isoformat() if notification.read_at else None,
                    'related_entity_id': notification.related_entity_id,
                    'related_entity_type': notification.related_entity_type,
                    'sender_cpf': notification.sender_cpf,
                    'created_at': notification.created_at.isoformat()
                })
            
            return HttpResponse(
                status_code=200,
                body={
                    'notifications': notifications_data,
                    'total': len(notifications_data)
                }
            )
            
        except Exception as e:
            return HttpResponse(
                status_code=500,
                body={'error': f'Erro ao buscar notificações: {str(e)}'}
            )
