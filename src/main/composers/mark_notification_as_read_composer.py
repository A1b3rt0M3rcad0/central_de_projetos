from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.mark_notification_as_read_controller import MarkNotificationAsReadController
from src.data.use_cases.mark_notification_as_read import MarkNotificationAsRead
from src.infra.relational.repository.notification_repository import NotificationRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection


def mark_notification_as_read_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para marcar notificação como lida"""
    
    # Configuração para notificações (relational database)
    db_connection_handler = DBConnectionHandler(StringConnection())
    notification_repository = NotificationRepository(db_connection_handler)
    
    # Use case
    mark_notification_as_read_case = MarkNotificationAsRead(notification_repository)
    
    # Controller
    controller = MarkNotificationAsReadController(mark_notification_as_read_case)
    
    return controller.handle
