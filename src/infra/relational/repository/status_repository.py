from src.data.interface.i_status_repository import IStatusRepository
from typing import Dict, List
from src.domain.entities.status import StatusEntity
from src.infra.relational.models.status import Status
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from sqlalchemy.exc import DataError

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
    
    def find(self, status_id:int) -> StatusEntity:
        return None
    
    def find_all(self) -> List[StatusEntity]:
        return None
    
    def update(self, status_id:int, update_params:Dict) -> None:
        return None
    
    def delete(self, status_id:int) -> None:
        return None