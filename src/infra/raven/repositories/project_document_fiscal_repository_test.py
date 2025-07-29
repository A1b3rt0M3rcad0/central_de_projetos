#pylint:disable=all
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.documents.project_document_fiscal import ProjectDocumentsFiscal
from src.domain.value_objects.pdf import PDF
from src.domain.value_objects.document import Document
from datetime import datetime, timezone

def test_insert() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

    project_id = 999999999

    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:
        document = doc.read()
    
    now = datetime.now(timezone.utc).strftime('%d/%m/%Y')
    pdf = PDF(document, document_name='test_pdf')
    project_documents = ProjectDocumentsFiscal('Rua João Verde', 'Pavimentação da rua')

    # Inserir o documento
    project_document_repository.insert_documents(project_id=project_id, project_documents=project_documents, documents=[pdf])

    # Verificar se o documento foi inserido
    with db_connection_handler as db:
        key = f'ProjectDocumentsFiscal/{project_id}'
        entity = db.load(key)

        if entity is None:
            raise Exception(f'Documento com ID {project_id} não encontrado.')

        # Verificar metadados para anexos
        metadata = db.advanced.get_metadata_for(entity)
        attachments = metadata.get('@attachments', [])

        # Verificar se o anexo foi inserido corretamente
        assert any(att['Name'] == f'test_pdf__{now}' for att in attachments), \
            f"O anexo 'test_pdf' não foi encontrado no documento."

def test_get_document_names() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

    project_id = 999999999

    # Inserir um documento de teste para garantir que há anexos
    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:
        document = doc.read()
    
    pdf = PDF(document, document_name='test_pdf_get')
    project_documents = ProjectDocumentsFiscal('Rua João Verde', 'Pavimentação da rua')
    project_document_repository.insert_documents(project_id=project_id, project_documents=project_documents, documents=[pdf])

    # Obtém os nomes dos anexos
    document_names = project_document_repository.get_document_names(project_id=project_id)

    assert len(document_names) > 0, \
        f"Não foram encontrados anexos para o projeto com ID {project_id}."

    assert isinstance(document_names, list)
    assert all(isinstance(name, str) for name in document_names), \
        f"Alguns nomes dos anexos não são strings."

    now = datetime.now(timezone.utc).strftime('%d/%m/%Y')
    assert f'test_pdf_get__{now}.pdf' in document_names, \
        f"O nome do anexo 'test_pdf_get' não foi encontrado nos nomes dos anexos."

def test_get_document() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

    project_id = 999999999
    now = datetime.now(timezone.utc).strftime('%d/%m/%Y')
    document_name = f'test_pdf_get__{now}'

    # Obtém o documento
    document = project_document_repository.get_document(
        project_id=project_id,
        document_name=document_name,
        _document_class=PDF
    )
    assert document is not None, \
        f"O documento '{document_name}' não foi encontrado para o projeto com ID {project_id}."

    assert isinstance(document, Document)
    assert document.document_name == document_name, \
        f"O nome do documento retornado não corresponde ao nome esperado."

def test_delete() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

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