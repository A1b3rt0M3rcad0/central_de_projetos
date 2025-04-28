from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from sqlalchemy.exc import IntegrityError
from src.errors.repository.project_fiscal_already_exists import ProjectFiscalAlreadyExists

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