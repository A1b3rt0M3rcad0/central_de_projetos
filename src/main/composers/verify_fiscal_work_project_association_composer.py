from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.data.use_cases.verify_fiscal_work_project_association import VerifyFiscalWorkProjectAssociation

def verify_fiscal_work_project_association_composer() -> VerifyFiscalWorkProjectAssociation:
    return VerifyFiscalWorkProjectAssociation(
        work_project_repository=WorkProjectRepository(
            db_connection_handler=db_connection_handler_factory()
        )
    ) 