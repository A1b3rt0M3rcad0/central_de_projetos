from src.infra.relational.models.history_project import HistoryProject
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_history_project_repository import IHistoryProjectRepository
from src.domain.entities.history_project import HistoryProjectEntity
from typing import Optional, Dict, List

# Errors
from src.errors.repository.not_exists_error.project_not_exists import ProjectNotExistsError
from src.errors.repository.not_exists_error.history_project_not_exists import HistoryProjectNotExists
from src.errors.repository.error_on_insert.error_on_insert_history_project import ErrorOnInsertHistoryProject
from src.errors.repository.error_on_find.error_on_find_history_project import ErrorOnFindHistoryProject
from src.errors.repository.error_on_update.error_on_update_history_project import ErrorOnUpdateHistoryProject
from src.errors.repository.error_on_delete.error_on_delete_history_project import ErrorOnDeleteHistoryProject
from src.errors.repository.has_related_children.history_project_has_related_children import HistoryProjectHasRelatedChildren
from sqlalchemy.exc import IntegrityError

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
                raise ProjectNotExistsError(
                    message=f'Project {project_id} does not exists: {str(e)}'
                ) from e
            except Exception as e:
                raise ErrorOnInsertHistoryProject(message=f'Error on insert history project {project_id}: {str(e)}') from e
    
    def find(self, history_project_id:int) -> HistoryProjectEntity:
        with self.__db_connection_handler as db:
            try:
                history_project = db.session.query(HistoryProject).where(
                    HistoryProject.id == history_project_id
                ).first()
                if not history_project:
                    raise HistoryProjectNotExists(message=f'History project {history_project_id} does not exist')
                return HistoryProjectEntity(
                    history_project_id = history_project.id,
                    project_id = history_project.project_id,
                    data_name = history_project.data_name,
                    description = history_project.description,
                    updated_at = history_project.updated_at
                )
            except HistoryProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindHistoryProject(message=f'Error on find history project {history_project_id}: {str(e)}') from e
    
    def find_all_from_project(self, project_id:int) -> List[HistoryProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                full_history = db.session.query(HistoryProject).where(
                    HistoryProject.project_id == project_id
                ).all()
                if not any(full_history):
                    raise HistoryProjectNotExists(message=f'History from project {project_id} does not exist')
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
                raise ErrorOnFindHistoryProject(message=f'Error on find all history from project {project_id}: {str(e)}') from e
    
    def update(self, history_project_id:int, update_params:Dict) -> None:
        with self.__db_connection_handler as db:
            try:
                history_project = db.session.query(HistoryProject).where(
                    HistoryProject.id == history_project_id
                ).first()
                if not history_project:
                    raise HistoryProjectNotExists(f'History project not exists {history_project_id}')
                db.session.query(HistoryProject).where(
                    HistoryProject.id == history_project_id
                ).update(update_params)
                db.session.commit()
            except HistoryProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnUpdateHistoryProject(message=f'Error on update history_project {update_params}: {str(e)}') from e
    
    def delete(self, history_project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                history_project = db.session.query(HistoryProject).where(
                    HistoryProject.id == history_project_id
                ).first()
                if not history_project:
                    raise HistoryProjectNotExists(f'History project not exists {history_project_id}')
                db.session.query(HistoryProject).where(
                    HistoryProject.id == history_project_id
                ).delete()
                db.session.commit()
            except HistoryProjectNotExists as e:
                raise e from e
            except IntegrityError as e:
                raise HistoryProjectHasRelatedChildren(message=f'History project {history_project_id} has related children: {str(e)}') from e
            except Exception as e:
                raise ErrorOnDeleteHistoryProject(message=f'Error on delete history project {history_project_id}: {str(e)}') from e
    
    def delete_all_from_project(self, project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                history_project = db.session.query(HistoryProject).where(
                    HistoryProject.project_id == project_id
                ).first()
                if not history_project:
                    raise HistoryProjectNotExists(f'History project from project {project_id} not exists')
                db.session.query(HistoryProject).where(
                    HistoryProject.project_id == project_id
                ).delete()
                db.session.commit()
            except HistoryProjectNotExists as e:
                raise e from e
            except IntegrityError as e:
                raise HistoryProjectHasRelatedChildren(message=f'History project from project {project_id} has related children: {str(e)}') from e
            except Exception as e:
                raise ErrorOnDeleteHistoryProject(message=f'Error on delete all history from project {project_id}: {str(e)}') from e