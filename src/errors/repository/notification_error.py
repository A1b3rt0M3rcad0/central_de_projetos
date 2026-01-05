from src.errors.repository.__base.base_repository_error import BaseRepositoryError


class NotificationError(BaseRepositoryError):
    """Erro genérico relacionado a notificações"""
    
    def __init__(self, message: str = "Erro relacionado a notificações") -> None:
        super().__init__(
            title="NotificationError",
            message=message
        )
