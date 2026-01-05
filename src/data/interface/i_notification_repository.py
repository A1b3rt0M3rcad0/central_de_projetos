from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.notification import NotificationEntity, NotificationType
from datetime import datetime


class INotificationRepository(ABC):
    """Interface para repositório de notificações"""

    @abstractmethod
    def create(self, notification: NotificationEntity) -> int:
        """
        Cria uma nova notificação
        
        Args:
            notification: Entidade de notificação
            
        Returns:
            int: ID da notificação criada
        """
        pass

    @abstractmethod
    def find_by_recipient(
        self, 
        recipient_cpf: str, 
        limit: Optional[int] = None,
        offset: Optional[int] = None,
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

    @abstractmethod
    def find_by_id(self, notification_id: int) -> Optional[NotificationEntity]:
        """
        Busca notificação por ID
        
        Args:
            notification_id: ID da notificação
            
        Returns:
            Optional[NotificationEntity]: Notificação encontrada ou None
        """
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: int, read_at: datetime) -> bool:
        """
        Marca notificação como lida
        
        Args:
            notification_id: ID da notificação
            read_at: Data/hora da leitura
            
        Returns:
            bool: True se foi marcada como lida
        """
        pass

    @abstractmethod
    def mark_all_as_read(self, recipient_cpf: str, read_at: datetime) -> int:
        """
        Marca todas as notificações de um usuário como lidas
        
        Args:
            recipient_cpf: CPF do destinatário
            read_at: Data/hora da leitura
            
        Returns:
            int: Número de notificações marcadas como lidas
        """
        pass

    @abstractmethod
    def count_unread(self, recipient_cpf: str) -> int:
        """
        Conta notificações não lidas de um usuário
        
        Args:
            recipient_cpf: CPF do destinatário
            
        Returns:
            int: Número de notificações não lidas
        """
        pass

    @abstractmethod
    def find_by_type_and_recipient(
        self, 
        notification_type: NotificationType, 
        recipient_cpf: str,
        limit: Optional[int] = None
    ) -> List[NotificationEntity]:
        """
        Busca notificações por tipo e destinatário
        
        Args:
            notification_type: Tipo da notificação
            recipient_cpf: CPF do destinatário
            limit: Limite de resultados
            
        Returns:
            List[NotificationEntity]: Lista de notificações
        """
        pass

    @abstractmethod
    def delete_old_notifications(self, days_old: int = 30) -> int:
        """
        Remove notificações antigas
        
        Args:
            days_old: Número de dias para considerar como antigo
            
        Returns:
            int: Número de notificações removidas
        """
        pass
