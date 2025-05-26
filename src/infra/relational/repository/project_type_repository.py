#pylint:disable=W0611
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_project_type_repository import IProjectTypeRepository
from src.domain.entities.project_type import ProjectTypeEntity

from src.errors.repository.already_exists_error.project_type_already_exists import ProjectTypeAlreadyExists
from src.errors.repository.not_exists_error.projects_from_type_does_not_exists import ProjectsFromTypeDoesNotExists
from src.errors.repository.error_on_update.error_on_update_type_from_project import ErrorOnUpdateTypeFromProject
from src.errors.repository.error_on_delete.error_on_delete_project_type import ErrorOnDeleteProjectType

from src.infra.relational.models.types import Types
from src.infra.relational.models.project import Project

class ProjectTypeRepository(IProjectTypeRepository):
    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, project_id: int, type_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(ProjectType(project_id=project_id, type_id=type_id))
                db.session.commit()
        except IntegrityError as e:
            raise ProjectTypeAlreadyExists(
                message=f'ProjectType with (project_id: {project_id}, type_id: {type_id}) already exists: {e}'
            ) from e
        except Exception as e:
            raise e

    def find(self, project_id: int, type_id: int) -> ProjectTypeEntity:
        try:
            with self.__db_connection_handler as db:
                relation = db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).first()
                if not relation:
                    raise ProjectsFromTypeDoesNotExists(
                        message=f'No ProjectType with (project_id: {project_id}, type_id: {type_id}) found'
                    )
                return ProjectTypeEntity(
                    project_id=relation.project_id,
                    type_id=relation.type_id,
                    created_at=relation.created_at
                )
        except Exception as e:
            raise e

    def find_all_from_type(self, type_id: int) -> List[ProjectTypeEntity]:
        try:
            with self.__db_connection_handler as db:
                relations = db.session.query(ProjectType).where(
                    ProjectType.type_id == type_id
                ).all()
                if not relations:
                    raise ProjectsFromTypeDoesNotExists(
                        message=f'No projects found for type_id: {type_id}'
                    )
                return [
                    ProjectTypeEntity(
                        project_id=relation.project_id,
                        type_id=relation.type_id,
                        created_at=relation.created_at
                    ) for relation in relations
                ]
        except Exception as e:
            raise e

    def update_type(self, project_id: int, type_id: int, new_type_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).update({'type_id': new_type_id})
                db.session.commit()
        except Exception as e:
            raise ErrorOnUpdateTypeFromProject(
                message=f'Error updating ProjectType (project_id: {project_id}, type_id: {type_id}) to {new_type_id}'
            ) from e

    def delete(self, project_id: int, type_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).delete()
                db.session.commit()
        except Exception as e:
            raise ErrorOnDeleteProjectType(
                message=f'Error deleting ProjectType (project_id: {project_id}, type_id: {type_id}): {e}'
            ) from e

    def delete_all_from_project(self, project_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectType).where(
                    ProjectType.project_id == project_id,
                ).delete()
                db.session.commit()
        except Exception as e:
            raise ErrorOnDeleteProjectType(
                message=f'Error deleting ProjectType (project_id: {project_id}): {e}'
            ) from e
    
    def select_all_from_project(self, project_id:int) -> List[ProjectTypeEntity]:
        try:
            with self.__db_connection_handler as db:
                relations = db.session.query(ProjectType).where(
                    ProjectType.project_id == project_id,
                ).all()
                return [
                    ProjectTypeEntity(
                        project_id=relation.project_id,
                        type_id=relation.type_id,
                        created_at=relation.created_at
                    ) for relation in relations
                ]
        except Exception as e:
            raise e from e