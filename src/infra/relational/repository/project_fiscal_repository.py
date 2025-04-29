from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from sqlalchemy.exc import IntegrityError
from src.errors.repository.project_fiscal_already_exists import ProjectFiscalAlreadyExists
from src.domain.entities.project_fiscal import ProjectFiscalEntity
from typing import List
from src.errors.repository.projects_from_fiscal_does_not_exists import ProjectsFromFiscalDoesNotExists

class ProjectFiscalRepository():

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