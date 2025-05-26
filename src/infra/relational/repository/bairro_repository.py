from src.domain.entities.bairro import BairroEntity
from src.infra.relational.models.bairro import Bairro
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_bairro_repository import IBairroRepository

# Errors
from src.errors.repository.not_exists_error.bairro_not_exists import BairroNotExists
from src.errors.repository.already_exists_error.bairro_already_exists import BairroAlreadyExists
from src.errors.repository.error_on_delete.error_on_delete_bairro import ErrorOnDeleteBairro
from src.errors.repository.error_on_insert.error_on_insert_bairro import ErrorOnInsertBairro
from src.errors.repository.error_on_find.error_on_find_bairro import ErrorOnFindBairro
from src.errors.repository.error_on_update.error_on_update_bairro import ErrorOnUpdateBairro
from src.errors.repository.has_related_children.bairro_has_related_children import BairroHasRelatedChildren
from sqlalchemy.exc import IntegrityError

class BairroRepository(IBairroRepository):

    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(Bairro(name=name))
                db.session.commit()
        except IntegrityError as e:
            raise BairroAlreadyExists(message=f'Bairro {name} already exists: {str(e)}') from e
        except Exception as e:
            raise ErrorOnInsertBairro(message=f'Error on insert bairro {name}: {str(e)}') from e

    def find_by_name(self, name: str) -> BairroEntity:
        try:
            with self.__db_connection_handler as db:
                bairro = db.session.query(Bairro).where(
                    Bairro.name == name
                ).first()
                if bairro is None:
                    raise BairroNotExists(message=f'Bairro with name "{name}" does not exist')
                return BairroEntity(
                    bairro_id=bairro.id,
                    name=bairro.name,
                    created_at=bairro.created_at
                )
        except BairroNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindBairro(message=f'Error on find bairro by name {name}: {str(e)}') from e
    
    def find_by_id(self, bairro_id:int) -> BairroEntity:
        try:
            with self.__db_connection_handler as db:
                bairro = db.session.query(Bairro).where(
                    Bairro.id == bairro_id
                ).first()
                if bairro is None:
                    raise BairroNotExists(message=f'bairro with id "{bairro_id}" does not exists')
                return BairroEntity(
                    bairro_id=bairro.id,
                    name=bairro.name,
                    created_at=bairro.created_at
                )
        except BairroNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindBairro(message=f'Error on find bairro by id {bairro_id}: {str(e)}') from e

    def update(self, name: str, new_name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                bairro = db.session.query(Bairro).where(Bairro.name == name).first()
                if bairro is None:
                    raise BairroNotExists(message=f'Bairro "{name}" does not exist')

                bairro.name = new_name
                db.session.commit()
        except IntegrityError as e:
            raise BairroAlreadyExists(message=f'Bairro "{new_name}" already exists: {str(e)}') from e
        except Exception as e:
            raise ErrorOnUpdateBairro(message=f'Error on update bairro {name} -> {new_name}: {str(e)}') from e

    def delete(self, name: str) -> None:
        try:
            with self.__db_connection_handler as db:
                bairro = db.session.query(Bairro).where(Bairro.name == name).first()
                if not bairro:
                    raise BairroNotExists(message=f'Bairro "{name}" does not exist')
                db.session.delete(bairro)
                db.session.commit()
        except BairroNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise BairroHasRelatedChildren(message=f'Bairro {name} not deleted because has a related children: {str(e)}') from e
        except Exception as e:
            raise ErrorOnDeleteBairro(message=f'Error on delete bairro {name}: {str(e)}') from e
