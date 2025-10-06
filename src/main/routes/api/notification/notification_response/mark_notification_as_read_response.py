from pydantic import BaseModel


class MarkNotificationAsReadResponse(BaseModel):
    """Resposta para marcar notificação como lida"""
    message: str
