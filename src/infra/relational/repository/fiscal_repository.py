from src.domain.entities.fiscal import FiscalEntity
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.errors.repository.fiscal_not_exists import FiscalNotExists
from src.errors.repository.fiscal_already_exists import FiscalAlreadyExists
from src.data.interface.i_fiscal_repository import IFiscalRepository

class FiscalRepository(IFiscalRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                fiscal = db.session.query(Fiscal).where(
                    Fiscal.name == name
                ).first()
                if fiscal:
                    raise FiscalAlreadyExists('The fiscal with this name already exists')
                db.session.add(
                    Fiscal(name=name)
                )
                db.session.commit()
        except Exception as e:
            raise e

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
        except Exception as e:
            raise e
     
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
        except Exception as e:
            raise e
    
    def update(self, name:str, new_name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(Fiscal).where(
                    Fiscal.name == name
                ).update({'name':new_name})
                db.session.commit()
        except Exception as e:
            raise e
    
    def delete(self, name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(Fiscal).where(
                    Fiscal.name == name
                ).delete()
                db.session.commit()
        except Exception as e:
            raise e