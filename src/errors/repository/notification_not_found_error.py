from src.errors.repository.__base.base_repository_error import BaseRepositoryError


class NotificationNotFoundError(BaseRepositoryError):
    """Erro quando uma notificação não é encontrada"""
    
    def __init__(self, message: str = "Notificação não encontrada") -> None:
        super().__init__(
            title="NotificationNotFoundError",
            message=message
        )
