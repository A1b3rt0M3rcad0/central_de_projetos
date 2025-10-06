from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class NotificationData(BaseModel):
    """Dados de uma notificação"""
    notification_id: Optional[int] = None
    recipient_cpf: str
    notification_type: str
    title: str
    message: str
    is_read: bool
    read_at: Optional[datetime] = None
    related_entity_id: Optional[int] = None
    related_entity_type: Optional[str] = None
    sender_cpf: Optional[str] = None
    created_at: datetime


class FindNotificationsResponse(BaseModel):
    """Resposta para busca de notificações"""
    notifications: List[NotificationData]
    total: int
