from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.documents.project_documents import ProjectDocuments
from src.domain.value_objects.pdf import PDF

def test_insert() -> None:

    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentRepository(db_connection_handler)

    with open('src/infra/raven/repositories/__test/001-1.pdf', 'rb') as doc:
        document = doc.read()
    
    pdf = PDF(document, document_name='test_pdf')
    project_documents = ProjectDocuments('Rua joao verde', 'pavimentação da rua')

    project_document_repository.insert_documents(project_id=999999999, project_documents=project_documents, documents=[pdf])
