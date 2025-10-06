from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_count_unread_notifications import ICountUnreadNotifications


class CountUnreadNotificationsController(ControllerInterface):
    """Controller para contar notificações não lidas"""

    def __init__(self, count_unread_notifications_case: ICountUnreadNotifications) -> None:
        self.__count_unread_notifications_case = count_unread_notifications_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """Handle para contar notificações não lidas"""
        try:
            # Extrair dados da requisição (query params)
            recipient_cpf = http_request.query_params.get('recipient_cpf')
            
            if not recipient_cpf:
                return HttpResponse(
                    status_code=400,
                    body={'error': 'recipient_cpf é obrigatório'}
                )
            
            # Contar notificações não lidas
            count = self.__count_unread_notifications_case.count(recipient_cpf)
            
            return HttpResponse(
                status_code=200,
                body={
                    'unread_count': count,
                    'recipient_cpf': recipient_cpf
                }
            )
            
        except Exception as e:
            return HttpResponse(
                status_code=500,
                body={'error': f'Erro ao contar notificações não lidas: {str(e)}'}
            )
