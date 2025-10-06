from pydantic import BaseModel


class CountUnreadNotificationsResponse(BaseModel):
    """Resposta para contar notificações não lidas"""
    unread_count: int
    recipient_cpf: str
