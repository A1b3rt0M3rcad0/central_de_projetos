from datetime import datetime
from typing import Optional
from enum import Enum


class NotificationType(Enum):
    """Tipos de notificação disponíveis no sistema"""
    WORK_PROJECT_CREATED = "WORK_PROJECT_CREATED"
    SYSTEM_ALERT = "SYSTEM_ALERT"
    ADMIN_MESSAGE = "ADMIN_MESSAGE"
    PROJECT_UPDATE = "PROJECT_UPDATE"
    FISCAL_ALERT = "FISCAL_ALERT"


class NotificationEntity:
    """Entidade que representa uma notificação no sistema"""

    def __init__(
        self,
        recipient_cpf: str,
        notification_type: NotificationType,
        title: str,
        message: str,
        created_at: datetime,
        is_read: bool = False,
        read_at: Optional[datetime] = None,
        related_entity_id: Optional[int] = None,
        related_entity_type: Optional[str] = None,
        sender_cpf: Optional[str] = None,
        notification_id: Optional[int] = None
    ) -> None:
        self.notification_id = notification_id
        self.recipient_cpf = recipient_cpf
        self.notification_type = notification_type
        self.title = title
        self.message = message
        self.created_at = created_at
        self.is_read = is_read
        self.read_at = read_at
        self.related_entity_id = related_entity_id
        self.related_entity_type = related_entity_type
        self.sender_cpf = sender_cpf

    def mark_as_read(self, read_at: datetime) -> None:
        """Marca a notificação como lida"""
        self.is_read = True
        self.read_at = read_at

    def is_work_project_notification(self) -> bool:
        """Verifica se é uma notificação de work project"""
        return self.notification_type == NotificationType.WORK_PROJECT_CREATED

    def is_admin_notification(self) -> bool:
        """Verifica se é uma notificação para admin"""
        return self.notification_type in [
            NotificationType.WORK_PROJECT_CREATED,
            NotificationType.SYSTEM_ALERT,
            NotificationType.ADMIN_MESSAGE
        ]

    def is_fiscal_notification(self) -> bool:
        """Verifica se é uma notificação para fiscal"""
        return self.notification_type in [
            NotificationType.SYSTEM_ALERT,
            NotificationType.ADMIN_MESSAGE,
            NotificationType.PROJECT_UPDATE,
            NotificationType.FISCAL_ALERT
        ]
