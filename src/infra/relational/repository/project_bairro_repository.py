from src.infra.relational.models.project_bairro import ProjectBairro
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from sqlalchemy.exc import IntegrityError
from src.domain.entities.project_bairro import ProjectBairroEntity
from src.errors.repository.project_bairro_already_exists import ProjectBairroAlreadyExists
from src.errors.repository.projects_from_bairro_does_not_exists import ProjectsFromBairroDoesNotExists
from src.errors.repository.error_on_update_bairro_from_project import ErrorOnUpdateBairroFromProject
from src.errors.repository.error_on_delete_project_bairro import ErrorOnDeleteProjectBairro
from src.data.interface.i_project_bairro_repository import IProjectBairroRepository
from typing import List
from sqlalchemy import and_

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
            raise e

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
                    raise ProjectsFromBairroDoesNotExists(
                        message=f'No association found for project_id={project_id} and bairro_id={bairro_id}'
                    )
                return ProjectBairroEntity(
                    project_id=assoc.project_id,
                    bairro_id=assoc.bairro_id,
                    created_at=assoc.created_at
                )
        except Exception as e:
            raise e

    def find_all_from_bairro(self, bairro_id: int) -> List[ProjectBairroEntity]:
        try:
            with self.__db_connection_handler as db:
                associations = db.session.query(ProjectBairro).filter(
                    ProjectBairro.bairro_id == bairro_id
                ).all()
                if not associations:
                    raise ProjectsFromBairroDoesNotExists(
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
        except Exception as e:
            raise e

    def update_bairro(self, project_id: int, bairro_id: int, new_bairro_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectBairro).filter(
                    and_(
                        ProjectBairro.project_id == project_id,
                        ProjectBairro.bairro_id == bairro_id
                    )
                ).update({'bairro_id': new_bairro_id})
                db.session.commit()
        except Exception as e:
            raise ErrorOnUpdateBairroFromProject(
                message=f'Error updating project {project_id} from bairro {bairro_id} to {new_bairro_id}'
            ) from e

    def delete(self, project_id: int, bairro_id: int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectBairro).filter(
                    and_(
                        ProjectBairro.project_id == project_id,
                        ProjectBairro.bairro_id == bairro_id
                    )
                ).delete()
                db.session.commit()
        except Exception as e:
            raise ErrorOnDeleteProjectBairro(
                message=f'Error deleting association (project_id={project_id}, bairro_id={bairro_id}): {e}'
            ) from e
    
    def delete_all_from_project(self, project_id:int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectBairro).filter(
                    ProjectBairro.project_id == project_id,
                ).delete()
                db.session.commit()
        except Exception as e:
            raise ErrorOnDeleteProjectBairro(
                message=f'Error deleting association (project_id={project_id}): {e}'
            ) from e