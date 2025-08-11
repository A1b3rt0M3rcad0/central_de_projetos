from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.main.config.database.raven_connection_handler_factory import raven_connection_handler_factory
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.data.use_cases.get_latest_work_project_image import GetLatestWorkProjectImage
from src.data.use_cases.verify_fiscal_work_project_association import VerifyFiscalWorkProjectAssociation
from src.presentation.controllers.get_work_project_thumbnail_controller import GetWorkProjectThumbnailController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_work_project_thumbnail_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetWorkProjectThumbnailController(
        get_latest_work_project_image_case=GetLatestWorkProjectImage(
            project_document_fiscal_repository=ProjectDocumentFiscalRepository(
                db_connection_handler=raven_connection_handler_factory()
            ),
            work_project_repository=WorkProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        verify_fiscal_work_project_association_case=VerifyFiscalWorkProjectAssociation(
            work_project_repository=WorkProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle 