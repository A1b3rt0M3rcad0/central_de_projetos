from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.domain.entities.project_fiscal import ProjectFiscalEntity
from typing import List
from sqlalchemy import and_
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository

# Errors
from src.errors.repository.already_exists_error.project_fiscal_already_exists import ProjectFiscalAlreadyExists
from src.errors.repository.not_exists_error.projects_from_fiscal_does_not_exists import ProjectFiscalNotExists
from src.errors.repository.error_on_delete.error_on_update_project_fiscal import ErrorOnUpdateProjectFiscal
from src.errors.repository.error_on_delete.error_on_delete_project_fiscal import ErrorOnDeleteProjectFiscal
from src.errors.repository.error_on_insert.error_on_insert_project_fiscal import ErrorOnInsertProjectFiscal
from src.errors.repository.error_on_find.error_on_find_project_fiscal import ErrorOnFindProjectFiscal
from src.errors.repository.has_related_children.project_fiscal_has_related_children import ProjectFiscalhasRelatedChildren
from sqlalchemy.exc import IntegrityError

class ProjectFiscalRepository(IProjectFiscalRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, project_id:int, fiscal_id:int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.add(
                    ProjectFiscal(
                        project_id=project_id,
                        fiscal_id=fiscal_id
                    )
                )
                db.session.commit()
        except IntegrityError as e:
            raise ProjectFiscalAlreadyExists(message=f'ProjectFiscal with (project_id: {project_id}, fiscal_id: {fiscal_id}) already exists: {e}') from e
        except Exception as e:
            raise ErrorOnInsertProjectFiscal(
                message=f'Error on insert project fiscal project_id={project_id}'
            ) from e
    
    def find_all_from_fiscal(self, fiscal_id:int) -> List[ProjectFiscalEntity]:
        try:
            with self.__db_connection_handler as db:
                projects = db.session.query(ProjectFiscal).where(
                    ProjectFiscal.fiscal_id == fiscal_id
                ).all()
                if not projects:
                    raise ProjectFiscalNotExists(
                        message=f'Not exists project(s) from fiscal: {fiscal_id}'
                    )
                results = [
                    ProjectFiscalEntity(project_id=project_fiscal.project_id, fiscal_id=project_fiscal.fiscal_id, created_at=project_fiscal.created_at) for project_fiscal in projects
                ]
                return results
        except ProjectFiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectFiscal(
                message=f'Error on find project fiscal from fiscal fiscal_id={fiscal_id}: {str(e)}'
            ) from e
    
    def find(self, fiscal_id:int, project_id:int) -> ProjectFiscalEntity:
        try:
            with self.__db_connection_handler as db:
                project = db.session.query(ProjectFiscal).where(
                    and_(
                        ProjectFiscal.fiscal_id == fiscal_id,
                        ProjectFiscal.project_id == project_id
                    )
                ).first()
                if project is None:
                    raise ProjectFiscalNotExists(
                        message=f'The project fiscal association ({fiscal_id}, {project_id}) does not exists'
                    )
                return ProjectFiscalEntity(
                    project_id=project_id,
                    fiscal_id=fiscal_id,
                    created_at=project.created_at
                )
        except ProjectFiscalNotExists as e:
            raise e from e
        except Exception as e:
            raise ErrorOnFindProjectFiscal(
                message=f'Error on find project_fiscal project_id={project_id}, fiscal_id={fiscal_id}: {str(e)}'
            ) from e
    
    def update_fiscal(self, project_id:int, fiscal_id:int, new_fiscal_id:int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectFiscal).where(
                    and_(
                        ProjectFiscal.project_id == project_id,
                        ProjectFiscal.fiscal_id == fiscal_id
                    )
                ).update(
                    {
                        'fiscal_id': new_fiscal_id
                    }
                )
                db.session.commit()
        except IntegrityError as e:
            raise ProjectFiscalAlreadyExists(
                message=f'Project fiscal with project_id={project_id}, fiscal_id={new_fiscal_id} already exists: {str(e)}'
            ) from e
        except Exception as e:
            raise ErrorOnUpdateProjectFiscal(
                message=f'Error on update project_fiscal (project:{project_id}, fiscal:{fiscal_id}) to {new_fiscal_id}: {str(e)}'
            ) from e
    
    def delete(self, project_id:int, fiscal_id:int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectFiscal).where(
                    and_(
                        ProjectFiscal.project_id == project_id,
                        ProjectFiscal.fiscal_id == fiscal_id
                    )
                ).delete()
                db.session.commit()
        except IntegrityError as e:
            raise ProjectFiscalhasRelatedChildren(
                message=f'Project fiscal project_id={project_id}, fiscal_id={fiscal_id} has related children'
            ) from e
        except Exception as e:
            raise ErrorOnDeleteProjectFiscal(
                message=f'Error on delete project fiscal association: {e}'
            ) from e
    
    def delete_all_from_project(self, project_id:int) -> None:
        try:
            with self.__db_connection_handler as db:
                db.session.query(ProjectFiscal).where(
                    ProjectFiscal.project_id == project_id,
                ).delete()
                db.session.commit()
        except IntegrityError as e:
            raise ProjectFiscalhasRelatedChildren(
                message=f'Project fiscal from project project_id={project_id} has related children'
            ) from e
        except Exception as e:
            raise ErrorOnDeleteProjectFiscal(
                message=f'Error on delete project fiscal association: {e}'
            ) from e