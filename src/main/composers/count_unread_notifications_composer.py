from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.count_unread_notifications_controller import CountUnreadNotificationsController
from src.data.use_cases.count_unread_notifications import CountUnreadNotifications
from src.infra.relational.repository.notification_repository import NotificationRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection


def count_unread_notifications_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para contar notificações não lidas"""
    
    # Configuração para notificações (relational database)
    db_connection_handler = DBConnectionHandler(StringConnection())
    notification_repository = NotificationRepository(db_connection_handler)
    
    # Use case
    count_unread_notifications_case = CountUnreadNotifications(notification_repository)
    
    # Controller
    controller = CountUnreadNotificationsController(count_unread_notifications_case)
    
    return controller.handle
