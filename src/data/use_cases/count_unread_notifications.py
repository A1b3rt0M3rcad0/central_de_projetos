from src.domain.use_cases.i_count_unread_notifications import ICountUnreadNotifications
from src.data.interface.i_notification_repository import INotificationRepository


class CountUnreadNotifications(ICountUnreadNotifications):
    """Implementação do caso de uso para contar notificações não lidas"""

    def __init__(self, notification_repository: INotificationRepository) -> None:
        self.__notification_repository = notification_repository

    def count(self, recipient_cpf: str) -> int:
        """Conta notificações não lidas de um usuário"""
        try:
            return self.__notification_repository.count_unread(recipient_cpf)
        except Exception as e:
            raise e from e
