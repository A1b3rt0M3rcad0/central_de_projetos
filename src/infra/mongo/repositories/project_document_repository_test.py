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

    with db_connection_handler as db:
        if db is not None:
            project_document = db['projectdocument'].find_one(
                {'project_id': 1}
            )
            assert len(project_document['documents']) == 3

def test_find_project_document(db_connection_handler) -> None:
    project_document_repository = ProjectDocumentRepository(db_connection_handler)
    documents = project_document_repository.find_project_document(1)

    assert len(documents) == 3

def test_insert_documents_into_project(db_connection_handler) -> None:
    project_document_repository = ProjectDocumentRepository(db_connection_handler)

    # Novos documentos a serem inseridos
    new_documents = [
        Word(b'word_extra', 'doc_extra_word'),
        PDF(b'pdf_extra', 'doc_extra_pdf')
    ]

    updated_model = ProjectDocumentModel(
        project_id=1,
        documents=new_documents
    )

    # Inserção dos novos documentos no projeto existente
    project_document_repository.insert_documents_into_project(updated_model)

    with db_connection_handler as db:
        if db is not None:
            project_document = db['projectdocument'].find_one({'project_id': 1})
            assert project_document is not None
            assert len(project_document['documents']) == 5
            assert any(doc['document_name'] == 'doc_extra_word' for doc in project_document['documents'])
            assert any(doc['document_name'] == 'doc_extra_pdf' for doc in project_document['documents'])

def test_delete_document_from_project(db_connection_handler) -> None:
    project_document_repository = ProjectDocumentRepository(db_connection_handler)

    # Verifica que o documento a ser deletado existe inicialmente
    with db_connection_handler as db:
        if db is not None:
            project_document = db['projectdocument'].find_one({'project_id': 1})
            # Confirma que o documento que será deletado está presente
            assert any(doc['document_name'] == 'documento_assinado' for doc in project_document['documents'])

    # Deleta o documento
    project_document_repository.delete_document_from_project(1, 'documento_assinado')

    # Verifica que o documento foi removido
    with db_connection_handler as db:
        if db is not None:
            updated_project_document = db['projectdocument'].find_one({'project_id': 1})
            assert updated_project_document is not None
            # Verifica que o documento deletado não está mais presente
            assert all(doc['document_name'] != 'documento_assinado' for doc in updated_project_document['documents'])

def test_delete_all_documents_from_project(db_connection_handler) -> None:
    project_document_repository = ProjectDocumentRepository(db_connection_handler)

    # Cria um projeto com 3 documentos
    project_document_model = ProjectDocumentModel(
        project_id=2,
        documents=[
            Word(b'word_document', 'documento_assinado'),
            PDF(b'pdf_document', 'documento_autenticado'),
            Excel(b'excel_document', 'planilha_de_desenvolvimento')
        ]
    )
    project_document_repository.create_project_document(project_document_model)

    # Verifica que os 3 documentos foram inseridos no projeto
    with db_connection_handler as db:
        if db is not None:
            project_document = db['projectdocument'].find_one({'project_id': 2})
            assert len(project_document['documents']) == 3

    # Deleta todos os documentos do projeto com project_id=2
    project_document_repository.delete_all_documents_from_project(2)

    # Verifica que a lista de documentos está vazia após a deleção
    with db_connection_handler as db:
        if db is not None:
            updated_project_document = db['projectdocument'].find_one({'project_id': 2})
            assert updated_project_document is not None
            assert len(updated_project_document['documents']) == 0