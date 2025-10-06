from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_mark_notification_as_read import IMarkNotificationAsRead


class MarkNotificationAsReadController(ControllerInterface):
    """Controller para marcar notificação como lida"""

    def __init__(self, mark_notification_as_read_case: IMarkNotificationAsRead) -> None:
        self.__mark_notification_as_read_case = mark_notification_as_read_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """Handle para marcar notificação como lida"""
        try:
            # Extrair dados da requisição
            notification_id = http_request.body.get('notification_id')
            
            if not notification_id:
                return HttpResponse(
                    status_code=400,
                    body={'error': 'notification_id é obrigatório'}
                )
            
            # Marcar como lida
            success = self.__mark_notification_as_read_case.mark_as_read(notification_id)
            
            if success:
                return HttpResponse(
                    status_code=200,
                    body={'message': 'Notificação marcada como lida com sucesso'}
                )
            return HttpResponse(
                status_code=404,
                body={'error': 'Notificação não encontrada'}
            )
            
        except Exception as e:
            return HttpResponse(
                status_code=500,
                body={'error': f'Erro ao marcar notificação como lida: {str(e)}'}
            )
