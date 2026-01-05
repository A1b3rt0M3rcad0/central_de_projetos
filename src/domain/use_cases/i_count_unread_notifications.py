from abc import ABC, abstractmethod


class ICountUnreadNotifications(ABC):
    """Interface para contar notificações não lidas"""

    @abstractmethod
    def count(self, recipient_cpf: str) -> int:
        """
        Conta notificações não lidas de um usuário
        
        Args:
            recipient_cpf: CPF do destinatário
            
        Returns:
            int: Número de notificações não lidas
        """
        pass
