from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.notification import NotificationEntity


class IFindNotifications(ABC):
    """Interface para busca de notificações"""

    @abstractmethod
    def find_by_recipient(
        self,
        recipient_cpf: str,
        limit: int = None,
        offset: int = None,
        unread_only: bool = False
    ) -> List[NotificationEntity]:
        """
        Busca notificações por destinatário
        
        Args:
            recipient_cpf: CPF do destinatário
            limit: Limite de resultados
            offset: Offset para paginação
            unread_only: Se deve retornar apenas não lidas
            
        Returns:
            List[NotificationEntity]: Lista de notificações
        """
        pass
