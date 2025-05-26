from src.domain.entities.fiscal import FiscalEntity
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_fiscal_repository import IFiscalRepository

# Errors
from src.errors.repository.not_exists_error.fiscal_not_exists import FiscalNotExists
from src.errors.repository.already_exists_error.fiscal_already_exists import FiscalAlreadyExists
from src.errors.repository.error_on_insert.error_on_insert_fiscal import ErrorOnInsertFiscal
from src.errors.repository.error_on_find.error_on_find_fiscal import ErrorOnFindFiscal
from src.errors.repository.error_on_update.error_on_update_fiscal import ErroronUpdateFiscal
from src.errors.repository.error_on_delete.error_on_delete_fiscal import ErrorOnDeleteFiscal
from src.errors.repository.has_related_children.fiscal_has_related_children import FiscalHasRelatedChildren

from sqlalchemy.exc import IntegrityError

class FiscalRepository(IFiscalRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(
                    Fiscal(name=name)
                )
                db.session.commit()
        except IntegrityError as e:
            raise FiscalAlreadyExists(message=f'Fiscal {name} already exists: {str(e)}') from e
        except Exception as e:
            raise ErrorOnInsertFiscal(message=f'Error on insert fiscal {name}: {str(e)}') from e

    def find_by_name(self, name:str) -> FiscalEntity:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(
                    Fiscal.name == name
                ).first()
                if fiscal is None:
                    raise FiscalNotExists(message=f'The fiscal with name {name} does not exists')
                return FiscalEntity(
                    fiscal_id=fiscal.id,
                    name=fiscal.name,
                    created_at=fiscal.created_at
                )
        except FiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindFiscal(message=f'Error on find fiscal by name {name}: {str(e)}') from e
     
    def find_by_id(self, fiscal_id:int) -> FiscalEntity:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(
                    Fiscal.id == fiscal_id
                ).first()
                if fiscal is None:
                    raise FiscalNotExists(message=f'The fiscal with id {fiscal_id} does not exists')
                return FiscalEntity(
                    fiscal_id=fiscal.id,
                    name=fiscal.name,
                    created_at=fiscal.created_at
                )
        except FiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindFiscal(message=f'Error on find fiscal by id {fiscal_id}: {str(e)}') from e
    
    def update(self, name:str, new_name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(Fiscal.name == name).first()
                if not fiscal:
                    raise FiscalNotExists(message=f'Fiscal with name {name} does not exists')
                db.session.query(Fiscal).where(
                    Fiscal.name == name
                ).update({'name':new_name})
                db.session.commit()
        except FiscalNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise FiscalAlreadyExists(message=f'Fiscal with name {new_name} already exists: {str(e)}') from e
        except Exception as e:
            raise ErroronUpdateFiscal(message=f'Error on update fiscal {name} -> {new_name}: {str(e)}') from e
    
    def delete(self, name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(Fiscal.name == name).first()
                if not fiscal:
                    raise FiscalNotExists(message=f'Fiscal with name {name} does not exists')
                db.session.query(Fiscal).where(
                    Fiscal.name == name
                ).delete()
                db.session.commit()
        except FiscalNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise FiscalHasRelatedChildren(f'Fiscal {name} not deleted because has a related children: {str(e)}') from e
        except Exception as e:
            raise ErrorOnDeleteFiscal(message=f'Error on delete fiscal {name}: {str(e)}') from e