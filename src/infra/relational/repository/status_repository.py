from src.data.interface.i_status_repository import IStatusRepository
from typing import Dict, List
from src.domain.entities.status import StatusEntity
from src.infra.relational.models.status import Status
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from sqlalchemy.exc import DataError
from sqlalchemy import and_
from typing import Optional

class StatusRepository(IStatusRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, description:str) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.add(Status(
                    description=description
                ))
                db.session.commit()
            except DataError as e:
                raise ValueError(f'The entry is too long to column: {e}') from e
            except Exception as e:
                db.session.rollback()
                raise e
    
    def find(self, status_id:Optional[int]=None, description:Optional[str]=None) -> StatusEntity:
        status_id_entry = status_id
        description_entry = description
        with self.__db_connection_handler as db:
            try:
                if status_id_entry and description_entry:
                    result = db.session.query(Status).where(
                        and_(
                        Status.id == status_id_entry,
                        Status.description == description_entry
                        )
                    ).first()
                    return StatusEntity(
                        status_id = result.id,
                        description=result.description,
                        created_at=result.created_at
                    )
                if status_id_entry:
                    result = db.session.query(Status).where(
                        Status.id == status_id
                    ).first()
                    return StatusEntity(
                        status_id = result.id,
                        description=result.description,
                        created_at=result.created_at
                    )
                if description_entry:
                    result = db.session.query(Status).where(
                        Status.description == description_entry
                    ).first()
                    return StatusEntity(
                        status_id = result.id,
                        description=result.description,
                        created_at=result.created_at
                    )
                raise ValueError('status_id and description, entry error')
            except Exception as e:
                db.session.rollback()
                raise e

    def find_all(self) -> List[StatusEntity]:
        with self.__db_connection_handler as db:
            try:
                result = db.session.query(Status).all()
                status_entities = [
                    StatusEntity(
                        status_id=status.id,
                        description=status.description,
                        created_at=status.created_at
                    ) for status in result
                ]

                return status_entities
            except Exception as e:
                raise e
    
    def update(self, update_params:Dict, status_id:Optional[int]=None, description:Optional[str]=None) -> None:
        update_params_entry = update_params
        status_id_entry = status_id
        description_entry = description
        with self.__db_connection_handler as db:
            try:
                if status_id_entry and description_entry:
                    db.session.query(Status).where(
                        and_(
                            Status.id == status_id_entry,
                            Status.description == description_entry
                        )
                    ).update(update_params_entry)
                    db.session.commit()
                    return
                if status_id_entry:
                    db.session.query(Status).where(
                        Status.id == status_id_entry
                    ).update(update_params_entry)
                    db.session.commit()
                    return
                if description_entry:
                    db.session.query(Status).where(
                        Status.description == description_entry
                    ).update(update_params_entry)
                    db.session.commit()
                    return
                raise ValueError('status_id and description, entry error')
            except Exception as e:
                raise e

    def delete(self, status_id: Optional[int] = None, description: Optional[str] = None) -> None:
        status_id_entry = status_id
        description_entry = description

        with self.__db_connection_handler as db:
            try:
                if status_id_entry and description_entry:
                    db.session.query(Status).where(
                        and_(
                            Status.id == status_id_entry,
                            Status.description == description_entry
                        )
                    ).delete()
                    db.session.commit()
                    return

                if status_id_entry:
                    db.session.query(Status).where(
                        Status.id == status_id_entry
                    ).delete()
                    db.session.commit()
                    return

                if description_entry:
                    db.session.query(Status).where(
                        Status.description == description_entry
                    ).delete()
                    db.session.commit()
                    return

                raise ValueError('status_id and description, entry error')
            except Exception as e:
                db.session.rollback()
                raise e
