from abc import ABC, abstractmethod
from src.domain.entities.notification import NotificationType


class ICreateNotification(ABC):
    """Interface para criação de notificações"""

    @abstractmethod
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
        """
        Cria uma nova notificação
        
        Args:
            recipient_cpf: CPF do destinatário
            notification_type: Tipo da notificação
            title: Título da notificação
            message: Mensagem da notificação
            related_entity_id: ID da entidade relacionada (opcional)
            related_entity_type: Tipo da entidade relacionada (opcional)
            sender_cpf: CPF do remetente (opcional)
            
        Returns:
            int: ID da notificação criada
        """
        pass
