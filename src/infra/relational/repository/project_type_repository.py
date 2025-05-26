#pylint:disable=W0611
from typing import List
from sqlalchemy import and_

from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.data.interface.i_project_type_repository import IProjectTypeRepository
from src.domain.entities.project_type import ProjectTypeEntity

from src.infra.relational.models.types import Types
from src.infra.relational.models.project import Project

# Errors
from src.errors.repository.already_exists_error.project_type_already_exists import ProjectTypeAlreadyExists
from src.errors.repository.not_exists_error.project_type_not_exists import ProjectTypeNotExists
from src.errors.repository.error_on_delete.error_on_delete_project_type import ErrorOnDeleteProjectType
from src.errors.repository.error_on_find.error_on_find_project_type import ErrorOnFindProjectType
from src.errors.repository.error_on_insert.error_on_insert_project_type import ErrorOnInsertProjectType
from src.errors.repository.error_on_update.error_on_update_project_type import ErrorOnUpdateProjectType
from src.errors.repository.has_related_children.project_type_has_related_children import ProjectTypeHasRelatedChildren
from sqlalchemy.exc import IntegrityError

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
            raise ErrorOnInsertProjectType(
                message=f'Error on insert project type project_id={project_id}, type_id={type_id}: {str(e)}'
            ) from e

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
                    raise ProjectTypeNotExists(
                        message=f'No ProjectType with (project_id: {project_id}, type_id: {type_id}) found'
                    )
                return ProjectTypeEntity(
                    project_id=relation.project_id,
                    type_id=relation.type_id,
                    created_at=relation.created_at
                )
        except ProjectTypeNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectType(
                message=f'Error on find project type project_id={project_id}, type_id={type_id}: {str(e)}'
            ) from e


    def find_all_from_type(self, type_id: int) -> List[ProjectTypeEntity]:
        try:
            with self.__db_connection_handler as db:
                relations = db.session.query(ProjectType).where(
                    ProjectType.type_id == type_id
                ).all()
                if not relations:
                    raise ProjectTypeNotExists(
                        message=f'No projects found for type_id: {type_id}'
                    )
                return [
                    ProjectTypeEntity(
                        project_id=relation.project_id,
                        type_id=relation.type_id,
                        created_at=relation.created_at
                    ) for relation in relations
                ]
        except ProjectTypeNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectType(
                message=f'Error on find project_type with type_id={type_id}: {str(e)}'
            ) from e

    def update_type(self, project_id: int, type_id: int, new_type_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_type = db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).first()
                if not project_type:
                    raise ProjectTypeNotExists(
                        message=f'Project type project_id={project_id}, type_id={type_id} not exists'
                    )
                db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).update({'type_id': new_type_id})
                db.session.commit()
        except ProjectTypeNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise ProjectTypeAlreadyExists(
                message=f'Project type project_id={project_id}, type_id={new_type_id} already exists'
            ) from e
        except Exception as e:
            raise ErrorOnUpdateProjectType(
                message=f'Error updating ProjectType (project_id: {project_id}, type_id: {type_id}) to {new_type_id}'
            ) from e

    def delete(self, project_id: int, type_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_type = db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).first()
                if not project_type:
                    raise ProjectTypeNotExists(
                        message=f'Project type project_id={project_id}, type_id={type_id} not exists'
                    )
                db.session.query(ProjectType).where(
                    and_(
                        ProjectType.project_id == project_id,
                        ProjectType.type_id == type_id
                    )
                ).delete()
                db.session.commit()
        except ProjectTypeNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise ProjectTypeHasRelatedChildren(
                message=f'Project type from project project_id={project_id}, type_id={type_id} has related children'
            ) from e
        except Exception as e:
            raise ErrorOnDeleteProjectType(
                message=f'Error deleting ProjectType (project_id: {project_id}, type_id: {type_id}): {e}'
            ) from e

    def delete_all_from_project(self, project_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_type = db.session.query(ProjectType).where(
                    ProjectType.project_id == project_id,
                ).all()
                if not any(project_type):
                    raise ProjectTypeNotExists(
                        message=f'Project Type from project project_id={project_id} not exists'
                    )
                db.session.query(ProjectType).where(
                    ProjectType.project_id == project_id,
                ).delete()
                db.session.commit()
        except ProjectTypeNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise ProjectTypeHasRelatedChildren(
                message=f'Project type from project_id={project_id} has related children: {str(e)}'
            ) from e
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
                if not any(relations):
                    raise ProjectTypeNotExists(
                        message=f'Project type from project project_id={project_id} does not exists'
                    )
                return [
                    ProjectTypeEntity(
                        project_id=relation.project_id,
                        type_id=relation.type_id,
                        created_at=relation.created_at
                    ) for relation in relations
                ]
        except ProjectTypeNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectType(
                message=f'Error on find all from project project_id={project_id}: {str(e)}'
            ) from e