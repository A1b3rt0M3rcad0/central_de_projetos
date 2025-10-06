from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.find_notifications_controller import FindNotificationsController
from src.data.use_cases.find_notifications import FindNotifications
from src.infra.relational.repository.notification_repository import NotificationRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection


def find_notifications_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para buscar notificações"""
    
    # Configuração para notificações (relational database)
    db_connection_handler = DBConnectionHandler(StringConnection())
    notification_repository = NotificationRepository(db_connection_handler)
    
    # Use case
    find_notifications_case = FindNotifications(notification_repository)
    
    # Controller
    controller = FindNotificationsController(find_notifications_case)
    
    return controller.handle
