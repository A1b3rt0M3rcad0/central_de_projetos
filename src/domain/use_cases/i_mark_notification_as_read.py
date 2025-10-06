from abc import ABC, abstractmethod


class IMarkNotificationAsRead(ABC):
    """Interface para marcar notificação como lida"""

    @abstractmethod
    def mark_as_read(self, notification_id: int) -> bool:
        """
        Marca uma notificação como lida
        
        Args:
            notification_id: ID da notificação
            
        Returns:
            bool: True se foi marcada como lida
        """
        pass
