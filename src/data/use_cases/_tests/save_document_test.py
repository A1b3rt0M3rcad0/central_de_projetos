from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.data.use_cases.save_document import SaveDocument
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.raven.config.connection.data_connection import DataConnection
from src.domain.value_objects.pdf import PDF
import pytest

@pytest.fixture
def pdf() -> PDF:
    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:   
        document = doc.read()
    return PDF(document, document_name='test_pdf_case')


def test_save_document_case(pdf) -> None:
    save_document = SaveDocument(ProjectDocumentRepository(DBConnectionHandler(DataConnection())))

    save_document.save(
        1293861928637812637865,
        [pdf]
    )