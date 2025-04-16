from src.infra.mongo.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.mongo.config.connection.t_string_connection import TStringConnection
from src.infra.mongo.models.project_document_model import ProjectDocumentModel
from src.infra.mongo.repositories.project_document_repository import ProjectDocumentRepository
from src.domain.value_objects.word import Word
from src.domain.value_objects.pdf import PDF
from src.domain.value_objects.excel import Excel
import pytest

@pytest.fixture
def documents() -> list:
    return [
        Word(b'word_document', 'documento_assinado'),
        PDF(b'pdf_document', 'documento_autenticado'),
        Excel(b'excel_document', 'planilha_de_desenvolvimento')
    ]

@pytest.fixture
def project_document_model(documents) -> ProjectDocumentModel:
    return ProjectDocumentModel(
        project_id=1,
        documents=documents
    )

@pytest.fixture
def db_connection_handler() -> DBConnectionHandler:
    return DBConnectionHandler(TStringConnection())

def test_create_project_document(project_document_model, db_connection_handler) -> None:
    project_document_repository = ProjectDocumentRepository(db_connection_handler)
    project_document_repository.create_project_document(project_document_model)