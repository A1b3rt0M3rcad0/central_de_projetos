from src.domain.entities.types import TypesEntity
from src.infra.relational.models.types import Types
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler

from src.data.interface.i_types_repository import ITypesRepository
from typing import List

# Errors
from src.errors.repository.not_exists_error.types_not_exists import TypesNotExists
from src.errors.repository.already_exists_error.types_already_exists import TypesAlreadyExists
from src.errors.repository.error_on_delete.error_on_delete_status import ErrorOnDeleteStatus
from src.errors.repository.error_on_insert.error_on_insert_type import ErrorOnInsertType
from src.errors.repository.error_on_find.error_on_find_type import ErrorOnFindType
from src.errors.repository.error_on_update.error_on_update_types import ErrorOnUpdateTypes
from src.errors.repository.has_related_children.status_has_related_children import StatusHasRelatedChildren
from sqlalchemy.exc import IntegrityError

class TypesRepository(ITypesRepository):

    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                existing_type = db.session.query(Types).where(
                    Types.name == name
                ).first()
                if existing_type:
                    raise TypesAlreadyExists(f'Type with name "{name}" already exists')
                db.session.add(Types(name=name))
                db.session.commit()
        except Exception as e:
            raise ErrorOnInsertType(
                message=f'Error on insert type name={name}: {str(e)}'
            ) from e

    def find_by_name(self, name: str) -> TypesEntity:
        try:
            with self.__db_connection_handler as db:
                type_instance = db.session.query(Types).where(
                    Types.name == name
                ).first()
                if type_instance is None:
                    raise TypesNotExists(f'Type with name "{name}" does not exist')
                return TypesEntity(
                    types_id=type_instance.id,
                    name=type_instance.name,
                    created_at=type_instance.created_at
                )
        except Exception as e:
            raise ErrorOnFindType(
                message=f'Error on find types by name name={name}: {str(e)}'
            ) from e
    
    def find_all(self) -> List[TypesEntity]:
        try:
            with self.__db_connection_handler as db:
                types = db.session.query(Types).all()
                types_entities = [
                    TypesEntity(
                        types_id=entity.id,
                        name=entity.name,
                        created_at=entity.created_at
                    )
                    for entity in types
                ]
                return types_entities
        except Exception as e:
            raise ErrorOnFindType(
                message=f'Error on find all types: {str(e)}'
            ) from e

    def update(self, name: str, new_name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                types = db.session.query(Types).where(
                    Types.name == name
                ).first()
                if not types:
                    raise TypesNotExists(
                        message=f'Types with name={name} not exists'
                    )
                db.session.query(Types).where(
                    Types.name == name
                ).update({'name': new_name})
                db.session.commit()
        except TypesNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnUpdateTypes(
                message=f'Error on update types from name={name} to name={new_name}: {str(e)}'
            ) from e

    def delete(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(Types).where(
                    Types.name == name
                ).delete()
                db.session.commit()
        except IntegrityError as e:
            raise StatusHasRelatedChildren(message='the registry cannot be deleted because it has related children') from e
        except Exception as e:
            raise ErrorOnDeleteStatus(message=f'Error on delete status: {e}') from e