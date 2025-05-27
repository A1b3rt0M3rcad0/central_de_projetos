from src.data.interface.i_status_repository import IStatusRepository
from typing import List
from src.domain.entities.status import StatusEntity
from src.infra.relational.models.status import Status
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from sqlalchemy import and_
from typing import Optional

# Errors
from src.errors.repository.already_exists_error.status_already_exists import StatusAlreadyExists
from src.errors.repository.not_exists_error.status_not_exists import StatusNotExists
from src.errors.repository.has_related_children.status_has_related_children import StatusHasRelatedChildren
from src.errors.repository.error_on_delete.error_on_delete_status import ErrorOnDeleteStatus
from src.errors.repository.error_on_update.error_on_update_status import ErrorOnUpdateStatus
from src.errors.repository.error_on_find.error_on_find_status import ErrorOnFindStatus
from sqlalchemy.exc import DataError, IntegrityError

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
                raise ErrorOnFindStatus(
                    message=f'Error on find status status_id={status_id}, description={description}: {str(e)}'
                ) from e

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
                raise ErrorOnFindStatus(
                    message=f'Error on find all status: {str(e)}'
                ) from e
    
    def update(self, status_id: int, new_description: str) -> None:
        with self.__db_connection_handler as db:
            try:
                result = db.session.query(Status).filter(
                    Status.id == status_id
                ).update(
                    {Status.description: new_description}
                )

                if result == 0:
                    raise StatusNotExists(message=f'Status com id {status_id} não encontrado.')

                db.session.commit()

            except IntegrityError as e:
                raise StatusAlreadyExists(
                    message=f'Status "{new_description}" já existe: {e}'
                ) from e

            except Exception as e:
                raise ErrorOnUpdateStatus(
                    message=f'Erro on update status status_id={status_id}, description={new_description}: {str(e)}'
                ) from e


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
            except IntegrityError as e:
                raise StatusHasRelatedChildren(
                    message=f'Error on delete status status_id={status_id} because its has related children: {str(e)}'
                ) from e
            except Exception as e:
                raise ErrorOnDeleteStatus(
                    message=f'Error on delete status status_id={status_id}: {str(e)}'
                ) from e
