from src.infra.relational.models.history_project import HistoryProject
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_history_project import IHistoryProjectRepository
from src.domain.entities.user_project import UserProjectEntity
from typing import Optional, Dict, List

class HistoryProjectRepository(IHistoryProjectRepository):

    def __init__(self, db_connection_handler = IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, project_id:int, data_name:str, description:Optional[str] = None) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.add(
                    HistoryProject(
                        project_id=project_id,
                        data_name=data_name,
                        description=description
                    )
                )
                db.session.commit()
            except Exception as e:
                raise e
    
    def find(self, history_project_id:int) -> List[UserProjectEntity]:
        return None
    
    def find_all_from_project(self, project_id:int) -> List[UserProjectEntity]:
        return None
    
    def update(self, history_project_id:int, update_params:Dict) -> None:
        return None
    
    def delete(self, history_project_id:int) -> None:
        return None
    
