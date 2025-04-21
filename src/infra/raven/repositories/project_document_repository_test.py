#pylint:disable=all
from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.documents.project_documents import ProjectDocuments
from src.domain.value_objects.pdf import PDF
from src.domain.value_objects.word import Word
from src.domain.value_objects.excel import Excel

def test_insert() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentRepository(db_connection_handler)

    project_id = 999999999

    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:
        document = doc.read()
    
    pdf = PDF(document, document_name='test_pdf')
    project_documents = ProjectDocuments('Rua João Verde', 'Pavimentação da rua')

    # Inserir o documento
    project_document_repository.insert_documents(project_id=project_id, project_documents=project_documents, documents=[pdf])

    # Verificar se o documento foi inserido
    with db_connection_handler as db:
        key = f'ProjectDocuments/{project_id}'
        entity = db.load(key)

        if entity is None:
            raise Exception(f'Documento com ID {project_id} não encontrado.')

        # Verificar metadados para anexos
        metadata = db.advanced.get_metadata_for(entity)
        attachments = metadata.get('@attachments', [])

        # Verificar se o anexo foi inserido corretamente
        assert any(att['Name'] == 'test_pdf' for att in attachments), \
            f"O anexo 'test_pdf' não foi encontrado no documento."

def test_get_document_names() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentRepository(db_connection_handler)

    project_id = 999999999

    # Inserir um documento de teste para garantir que há anexos
    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:
        document = doc.read()
    
    pdf = PDF(document, document_name='test_pdf_get')
    project_documents = ProjectDocuments('Rua João Verde', 'Pavimentação da rua')
    project_document_repository.insert_documents(project_id=project_id, project_documents=project_documents, documents=[pdf])

    # Obtém os nomes dos anexos
    document_names = project_document_repository.get_document_names(project_id=project_id)

    assert len(document_names) > 0, \
        f"Não foram encontrados anexos para o projeto com ID {project_id}."

def test_get_document() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentRepository(db_connection_handler)

    project_id = 999999999
    document_name = 'test_pdf_get'

    # Obtém o documento
    document = project_document_repository.get_document(
        project_id=project_id,
        document_name=document_name 
    )
    assert document is not None, \
        f"O documento '{document_name}' não foi encontrado para o projeto com ID {project_id}."

    assert isinstance(document, dict)

def test_delete() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentRepository(db_connection_handler)

    project_id = 999999999
    document_name = 'test_pdf'

    # Deleta o anexo
    project_document_repository.delete_document(
        project_id=project_id,
        document_name=document_name
    )

    # Verifica se foi deletado
    with db_connection_handler as db:
        key = f'ProjectDocuments/{project_id}'
        entity = db.load(key)

        if entity is None:
            raise Exception(f'Documento com ID {project_id} não encontrado.')

        metadata = db.advanced.get_metadata_for(entity)
        attachments = metadata.get('@attachments', [])

        assert all(att['Name'] != document_name for att in attachments), \
            f"O anexo '{document_name}' ainda está presente no documento."