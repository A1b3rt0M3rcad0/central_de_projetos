from typing import List
from src.domain.use_cases.i_find_notifications import IFindNotifications
from src.domain.entities.notification import NotificationEntity
from src.data.interface.i_notification_repository import INotificationRepository


class FindNotifications(IFindNotifications):
    """Implementação do caso de uso para busca de notificações"""

    def __init__(self, notification_repository: INotificationRepository) -> None:
        self.__notification_repository = notification_repository

    def find_by_recipient(
        self,
        recipient_cpf: str,
        limit: int = None,
        offset: int = None,
        unread_only: bool = False
    ) -> List[NotificationEntity]:
        """Busca notificações por destinatário"""
        try:
            return self.__notification_repository.find_by_recipient(
                recipient_cpf=recipient_cpf,
                limit=limit,
                offset=offset,
                unread_only=unread_only
            )
        except Exception as e:
            raise e from e
