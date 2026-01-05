from datetime import datetime
from src.domain.use_cases.i_mark_notification_as_read import IMarkNotificationAsRead
from src.data.interface.i_notification_repository import INotificationRepository


class MarkNotificationAsRead(IMarkNotificationAsRead):
    """Implementação do caso de uso para marcar notificação como lida"""

    def __init__(self, notification_repository: INotificationRepository) -> None:
        self.__notification_repository = notification_repository

    def mark_as_read(self, notification_id: int) -> bool:
        """Marca uma notificação como lida"""
        try:
            return self.__notification_repository.mark_as_read(
                notification_id=notification_id,
                read_at=datetime.now()
            )
        except Exception as e:
            raise e from e
