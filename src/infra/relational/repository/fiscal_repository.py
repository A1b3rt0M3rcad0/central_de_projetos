#from src.domain.entities.fiscal import FiscalEntity
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler

class FiscalRepository():

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, name:str) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(
                    Fiscal(name=name)
                )
                db.session.commit()
        except Exception as e:
            raise e
