from typing import List, Optional
from src.data.interface.i_notification_repository import INotificationRepository
from src.domain.entities.notification import NotificationEntity, NotificationType
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.models.notification import Notification
from src.errors.repository.notification_error import NotificationError
from src.errors.repository.notification_not_found_error import NotificationNotFoundError
from datetime import datetime, timedelta


class NotificationRepository(INotificationRepository):
    """Implementação do repositório de notificações usando SQLAlchemy"""

    def __init__(self, db_connection_handler: DBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def create(self, notification: NotificationEntity) -> int:
        """Cria uma nova notificação"""
        try:
            with self.__db_connection_handler as session:
                db_notification = Notification(
                    recipient_cpf=notification.recipient_cpf,
                    notification_type=notification.notification_type.value,
                    title=notification.title,
                    message=notification.message,
                    is_read=notification.is_read,
                    read_at=notification.read_at,
                    related_entity_id=notification.related_entity_id,
                    related_entity_type=notification.related_entity_type,
                    sender_cpf=notification.sender_cpf,
                    created_at=notification.created_at
                )
                
                session.session.add(db_notification)
                session.session.commit()
                session.session.refresh(db_notification)
                
                return db_notification.id
                
        except Exception as e:
            raise NotificationError(f"Erro ao criar notificação: {str(e)}") from e

    def find_by_recipient(
        self, 
        recipient_cpf: str, 
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        unread_only: bool = False
    ) -> List[NotificationEntity]:
        """Busca notificações por destinatário"""
        try:
            with self.__db_connection_handler as session:
                query = session.session.query(Notification).filter(
                    Notification.recipient_cpf == recipient_cpf
                )
                
                if unread_only:
                    query = query.filter(Notification.is_read.is_(False))
                
                query = query.order_by(Notification.created_at.desc())
                
                if offset:
                    query = query.offset(offset)
                
                if limit:
                    query = query.limit(limit)
                
                db_notifications = query.all()
                
                return [
                    self.__convert_to_entity(db_notification)
                    for db_notification in db_notifications
                ]
                
        except Exception as e:
            raise NotificationError(f"Erro ao buscar notificações: {str(e)}") from e

    def find_by_id(self, notification_id: int) -> Optional[NotificationEntity]:
        """Busca uma notificação por ID"""
        try:
            with self.__db_connection_handler as session:
                db_notification = session.session.query(Notification).filter(
                    Notification.id == notification_id
                ).first()
                
                if not db_notification:
                    return None
                
                return self.__convert_to_entity(db_notification)
                
        except NotificationNotFoundError:
            raise
        except Exception as e:
            raise NotificationError(f"Erro ao buscar notificação: {str(e)}") from e

    def mark_as_read(self, notification_id: int, read_at: datetime) -> bool:
        """Marca uma notificação como lida"""
        try:
            with self.__db_connection_handler as session:
                db_notification = session.session.query(Notification).filter(
                    Notification.id == notification_id
                ).first()
                
                if not db_notification:
                    raise NotificationNotFoundError(f"Notificação com ID {notification_id} não encontrada")
                
                db_notification.is_read = True
                db_notification.read_at = read_at
                
                session.session.commit()
                return True
                
        except NotificationNotFoundError:
            raise
        except Exception as e:
            raise NotificationError(f"Erro ao marcar notificação como lida: {str(e)}") from e

    def mark_all_as_read(self, recipient_cpf: str, read_at: datetime) -> int:
        """Marca todas as notificações de um destinatário como lidas"""
        try:
            with self.__db_connection_handler as session:
                result = session.session.query(Notification).filter(
                    Notification.recipient_cpf == recipient_cpf,
                    Notification.is_read.is_(False)
                ).update({
                    'is_read': True,
                    'read_at': read_at
                })
                
                session.session.commit()
                return result
                
        except Exception as e:
            raise NotificationError(f"Erro ao marcar todas as notificações como lidas: {str(e)}") from e

    def count_unread(self, recipient_cpf: str) -> int:
        """Conta notificações não lidas de um destinatário"""
        try:
            with self.__db_connection_handler as session:
                count = session.session.query(Notification).filter(
                    Notification.recipient_cpf == recipient_cpf,
                    Notification.is_read.is_(False)
                ).count()
                
                return count
                
        except Exception as e:
            raise NotificationError(f"Erro ao contar notificações não lidas: {str(e)}") from e

    def delete_old_notifications(self, days_old: int = 30) -> int:
        """Remove notificações antigas"""
        try:
            with self.__db_connection_handler as session:
                cutoff_date = datetime.now() - timedelta(days=days_old)
                
                result = session.session.query(Notification).filter(
                    Notification.created_at < cutoff_date
                ).delete()
                
                session.session.commit()
                return result
                
        except Exception as e:
            raise NotificationError(f"Erro ao deletar notificações antigas: {str(e)}") from e

    def find_by_type_and_recipient(
        self, 
        notification_type: NotificationType, 
        recipient_cpf: str,
        limit: Optional[int] = None
    ) -> List[NotificationEntity]:
        """Busca notificações por tipo e destinatário"""
        try:
            with self.__db_connection_handler as session:
                query = session.session.query(Notification).filter(
                    Notification.notification_type == notification_type.value,
                    Notification.recipient_cpf == recipient_cpf
                ).order_by(Notification.created_at.desc())
                
                if limit:
                    query = query.limit(limit)
                
                db_notifications = query.all()
                
                return [
                    self.__convert_to_entity(db_notification)
                    for db_notification in db_notifications
                ]
                
        except Exception as e:
            raise NotificationError(f"Erro ao buscar notificações por tipo e destinatário: {str(e)}") from e

    def __convert_to_entity(self, db_notification: Notification) -> NotificationEntity:
        """Converte um modelo SQLAlchemy para entidade de domínio"""
        return NotificationEntity(
            notification_id=db_notification.id,
            recipient_cpf=db_notification.recipient_cpf,
            notification_type=NotificationType(db_notification.notification_type),
            title=db_notification.title,
            message=db_notification.message,
            created_at=db_notification.created_at,
            is_read=db_notification.is_read,
            read_at=db_notification.read_at,
            related_entity_id=db_notification.related_entity_id,
            related_entity_type=db_notification.related_entity_type,
            sender_cpf=db_notification.sender_cpf
        )