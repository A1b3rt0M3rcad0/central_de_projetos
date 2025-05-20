from src.infra.relational.models.history_project import HistoryProject
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_history_project_repository import IHistoryProjectRepository
from src.domain.entities.history_project import HistoryProjectEntity
from src.errors.repository.project_id_not_exists import ProjectIdNotExistsError
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, List

class HistoryProjectRepository(IHistoryProjectRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
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
            except IntegrityError as e:
                raise ProjectIdNotExistsError(
                    message=f'Project {project_id} does not exists: {e}'
                ) from e
    
    def find(self, history_project_id:int) -> HistoryProjectEntity:
        with self.__db_connection_handler as db:
            try:
                history_project = db.session.query(HistoryProject).where(
                    HistoryProject.id == history_project_id
                ).first()
                return HistoryProjectEntity(
                    history_project_id = history_project.id,
                    project_id = history_project.project_id,
                    data_name = history_project.data_name,
                    description = history_project.description,
                    updated_at = history_project.updated_at
                )
            except Exception as e:
                raise e
    
    def find_all_from_project(self, project_id:int) -> List[HistoryProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                full_history = db.session.query(HistoryProject).where(
                    HistoryProject.project_id == project_id
                ).all()
                return [
                    HistoryProjectEntity(
                        history_project_id=register.id,
                        data_name=register.data_name,
                        description=register.description,
                        project_id=register.project_id,
                        updated_at=register.updated_at
                    ) for register in full_history
                ]
            except Exception as e:
                raise e
    
    def update(self, history_project_id:int, update_params:Dict) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(HistoryProject).where(
                    HistoryProject.id == history_project_id
                ).update(update_params)
                db.session.commit()
            except Exception as e:
                raise e
    
    def delete(self, history_project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(HistoryProject).where(
                    HistoryProject.id == history_project_id
                ).delete()
                db.session.commit()
            except Exception as e:
                raise e
    
    def delete_all_from_project(self, project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(HistoryProject).where(
                    HistoryProject.project_id == project_id
                ).delete()
                db.session.commit()
            except Exception as e:
                raise e from e