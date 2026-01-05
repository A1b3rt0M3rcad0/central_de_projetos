from datetime import datetime
from src.domain.use_cases.i_create_notification import ICreateNotification
from src.domain.entities.notification import NotificationEntity, NotificationType
from src.data.interface.i_notification_repository import INotificationRepository


class CreateNotification(ICreateNotification):
    """Implementação do caso de uso para criação de notificações"""

    def __init__(self, notification_repository: INotificationRepository) -> None:
        self.__notification_repository = notification_repository

    def create(
        self,
        recipient_cpf: str,
        notification_type: NotificationType,
        title: str,
        message: str,
        related_entity_id: int = None,
        related_entity_type: str = None,
        sender_cpf: str = None
    ) -> int:
        """Cria uma nova notificação"""
        try:
            notification = NotificationEntity(
                recipient_cpf=recipient_cpf,
                notification_type=notification_type,
                title=title,
                message=message,
                created_at=datetime.now(),
                is_read=False,
                read_at=None,
                related_entity_id=related_entity_id,
                related_entity_type=related_entity_type,
                sender_cpf=sender_cpf
            )
            
            return self.__notification_repository.create(notification)
            
        except Exception as e:
            raise e from e
