from src.infra.relational.models.project_bairro import ProjectBairro
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.domain.entities.project_bairro import ProjectBairroEntity
from src.data.interface.i_project_bairro_repository import IProjectBairroRepository
from typing import List
from sqlalchemy import and_

## Errors
from src.errors.repository.already_exists_error.project_bairro_already_exists import ProjectBairroAlreadyExists
from src.errors.repository.not_exists_error.project_bairro_not_exists import ProjectBairroNotExists
from src.errors.repository.error_on_delete.error_on_update_bairro_from_project import ErrorOnUpdateBairroFromProject
from src.errors.repository.error_on_delete.error_on_delete_project_bairro import ErrorOnDeleteProjectBairro
from src.errors.repository.error_on_insert.error_on_insert_project_bairro import ErrorOnInsertProjectBairro
from src.errors.repository.error_on_find.error_on_find_project_bairro import ErrorOnFindProjectBairro
from src.errors.repository.has_related_children.project_bairro_has_related_children import ProjectBairroHasRelatedChildren
from sqlalchemy.exc import IntegrityError

class ProjectBairroRepository(IProjectBairroRepository):

    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def insert(self, project_id: int, bairro_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(ProjectBairro(project_id=project_id, bairro_id=bairro_id))
                db.session.commit()
        except IntegrityError as e:
            raise ProjectBairroAlreadyExists(
                message=f'Association (project_id={project_id}, bairro_id={bairro_id}) already exists.'
            ) from e
        except Exception as e:
            raise ErrorOnInsertProjectBairro(message=f'Error on insert project bairro (project_id {project_id}, bairro_id {bairro_id}): {str(e)}') from e

    def find(self, project_id: int, bairro_id: int) -> ProjectBairroEntity:
        try:
            with self.__db_connection_handler as db:
                assoc = db.session.query(ProjectBairro).filter(
                    and_(
                        ProjectBairro.project_id == project_id,
                        ProjectBairro.bairro_id == bairro_id
                    )
                ).first()
                if not assoc:
                    raise ProjectBairroNotExists(
                        message=f'No association found for project_id={project_id} and bairro_id={bairro_id}'
                    )
                return ProjectBairroEntity(
                    project_id=assoc.project_id,
                    bairro_id=assoc.bairro_id,
                    created_at=assoc.created_at
                )
        except ProjectBairroNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectBairro(message=f'Error on find project project_id={project_id}, bairro_id={bairro_id}: {str(e)}') from e

    def find_all_from_bairro(self, bairro_id: int) -> List[ProjectBairroEntity]:
        try:
            with self.__db_connection_handler as db:
                associations = db.session.query(ProjectBairro).filter(
                    ProjectBairro.bairro_id == bairro_id
                ).all()
                if not associations:
                    raise ProjectBairroNotExists(
                        message=f'No projects found for bairro_id={bairro_id}'
                    )
                return [
                    ProjectBairroEntity(
                        project_id=assoc.project_id,
                        bairro_id=assoc.bairro_id,
                        created_at=assoc.created_at
                    )
                    for assoc in associations
                ]
        except ProjectBairroNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectBairro(message=f'Error on find project from bairro, bairro_id={bairro_id}: {str(e)}') from e

    def update_bairro(self, project_id: int, bairro_id: int, new_bairro_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_bairro = db.session.query(ProjectBairro).filter(
                    and_(
                        ProjectBairro.project_id == project_id,
                        ProjectBairro.bairro_id == bairro_id
                    )
                ).first()
                if not project_bairro:
                    raise ProjectBairroNotExists(message=f'Project bairro project_id={project_bairro}, bairro_id={bairro_id} not exists')
                db.session.query(ProjectBairro).filter(
                    and_(
                        ProjectBairro.project_id == project_id,
                        ProjectBairro.bairro_id == bairro_id
                    )
                ).update({'bairro_id': new_bairro_id})
                db.session.commit()
        except ProjectBairroNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnUpdateBairroFromProject(
                message=f'Error updating project {project_id} from bairro {bairro_id} to {new_bairro_id}'
            ) from e

    def delete(self, project_id: int, bairro_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_bairro = db.session.query(ProjectBairro).filter(
                    and_(
                        ProjectBairro.project_id == project_id,
                        ProjectBairro.bairro_id == bairro_id
                    )
                ).first()
                if not project_bairro:
                    raise ProjectBairroNotExists(message=f'Project bairro project_id={project_bairro}, bairro_id={bairro_id} not exists')
                db.session.query(ProjectBairro).filter(
                    and_(
                        ProjectBairro.project_id == project_id,
                        ProjectBairro.bairro_id == bairro_id
                    )
                ).delete()
                db.session.commit()
        except IntegrityError as e:
            raise ProjectBairroHasRelatedChildren(message=f'Project bairro project_id={project_id}, bairro_id={bairro_id} has related children: {str(e)}') from e
        except ProjectBairroNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnDeleteProjectBairro(
                message=f'Error deleting association (project_id={project_id}, bairro_id={bairro_id}): {e}'
            ) from e
    
    def delete_all_from_project(self, project_id:int) -> None:
        try:
            with self.__db_connection_handler as db:
                project_bairro = db.session.query(ProjectBairro).filter(
                    and_(
                        ProjectBairro.project_id == project_id
                    )
                ).all()
                if not any(project_bairro):
                    raise ProjectBairroNotExists(message=f'Project bairro with project project_id={project_bairro} not exists')
                db.session.query(ProjectBairro).filter(
                    ProjectBairro.project_id == project_id,
                ).delete()
                db.session.commit()
        except ProjectBairroNotExists as e:
            raise e from e
        except IntegrityError as e:
            raise ProjectBairroHasRelatedChildren(message=f'Project bairro from project project_id={project_id} has related children: {str(e)}') from e
        except Exception as e:
            raise ErrorOnDeleteProjectBairro(
                message=f'Error deleting association (project_id={project_id}): {e}'
            ) from e