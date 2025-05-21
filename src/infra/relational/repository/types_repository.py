from src.domain.entities.types import TypesEntity
from src.infra.relational.models.types import Types
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler

from src.errors.repository.types_not_exists import TypesNotExists
from src.errors.repository.types_already_exists import TypesAlreadyExists
from src.data.interface.i_types_repository import ITypesRepository
from src.errors.repository.error_on_delete_status import ErrorOnDeleteStatus
from sqlalchemy.exc import IntegrityError
from src.errors.repository.status_has_related_children import StatusHasRelatedChildren

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
            raise e

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
            raise e

    def update(self, name: str, new_name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(Types).where(
                    Types.name == name
                ).update({'name': new_name})
                db.session.commit()
        except Exception as e:
            raise e

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