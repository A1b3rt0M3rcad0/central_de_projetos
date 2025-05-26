from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from sqlalchemy.exc import IntegrityError
from src.errors.repository.already_exists_error.project_fiscal_already_exists import ProjectFiscalAlreadyExists
from src.domain.entities.project_fiscal import ProjectFiscalEntity
from typing import List
from src.errors.repository.not_exists_error.projects_from_fiscal_does_not_exists import ProjectsFromFiscalDoesNotExists
from src.errors.repository.error_on_delete.error_on_update_fiscal_from_project import ErrorOnUpdateFiscalFromProject
from src.errors.repository.error_on_delete.error_on_delete_project_fiscal import ErrorOnDeleteProjectFiscal
from sqlalchemy import and_
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository

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
            raise e
    
    def find_all_from_fiscal(self, fiscal_id:int) -> List[ProjectFiscalEntity]:
        try:
            with self.__db_connection_handler as db:
                projects = db.session.query(ProjectFiscal).where(
                    ProjectFiscal.fiscal_id == fiscal_id
                ).all()
                if not projects:
                    raise ProjectsFromFiscalDoesNotExists(
                        message=f'Not exists project(s) from fiscal: {fiscal_id}'
                    )
                results = [
                    ProjectFiscalEntity(project_id=project_fiscal.project_id, fiscal_id=project_fiscal.fiscal_id, created_at=project_fiscal.created_at) for project_fiscal in projects
                ]
                return results
        except Exception as e:
            raise e from e
    
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
                    raise ProjectsFromFiscalDoesNotExists(
                        message=f'The project fiscal association ({fiscal_id}, {project_id}) does not exists'
                    )
                return ProjectFiscalEntity(
                    project_id=project_id,
                    fiscal_id=fiscal_id,
                    created_at=project.created_at
                )
        except Exception as e:
            raise e
    
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
        except Exception as e:
            raise ErrorOnUpdateFiscalFromProject(
                message=f'Error on update project_fiscal (project:{project_id}, fiscal:{fiscal_id}) to {new_fiscal_id}'
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
        except Exception as e:
            raise ErrorOnDeleteProjectFiscal(
                message=f'Error on delete project fiscal association: {e}'
            ) from e