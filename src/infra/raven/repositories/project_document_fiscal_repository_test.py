#pylint:disable=all
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.documents.project_document_fiscal import ProjectDocumentsFiscal
from src.domain.value_objects.pdf import PDF
from src.domain.value_objects.document import Document
from datetime import datetime, timezone

def test_insert_fiscal_documents() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

    work_project_id = 999999999
    fiscal_id = 123

    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:
        document = doc.read()
    
    pdf = PDF(document, document_name='test_pdf')
    documents = [pdf]

    # Inserir os documentos fiscais
    project_document_repository.insert_fiscal_documents(
        work_project_id=work_project_id, 
        documents=documents
    )

    # Verificar se o documento foi inserido
    with db_connection_handler as db:
        key = f'ProjectDocumentsFiscal/{work_project_id}'
        entity = db.load(key)

        if entity is None:
            raise Exception(f'Documento com work_project_id {work_project_id} não encontrado.')

        # Verificar metadados para anexos
        metadata = db.advanced.get_metadata_for(entity)
        attachments = metadata.get('@attachments', [])

        # Verificar se o anexo foi inserido corretamente
        assert any(att['Name'] == 'test_pdf' for att in attachments), \
            f"O anexo 'test_pdf' não foi encontrado no documento."

def test_get_fiscal_document_names() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

    work_project_id = 999999999
    fiscal_id = 123

    # Inserir um documento de teste para garantir que há anexos
    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:
        document = doc.read()
    
    pdf = PDF(document, document_name='test_pdf_get')
    documents = [pdf]
    project_document_repository.insert_fiscal_documents(
        work_project_id=work_project_id, 
        documents=documents
    )

    # Obtém os nomes dos anexos
    document_names = project_document_repository.get_fiscal_document_names(
        work_project_id=work_project_id, 
        fiscal_id=fiscal_id
    )

    assert len(document_names) > 0, \
        f"Não foram encontrados anexos para o work_project_id {work_project_id}."

    assert isinstance(document_names, list)
    assert all(isinstance(name, str) for name in document_names), \
        f"Alguns nomes dos anexos não são strings."

    assert 'test_pdf_get.pdf' in document_names, \
        f"O nome do anexo 'test_pdf_get' não foi encontrado nos nomes dos anexos."

def test_get_fiscal_document() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

    work_project_id = 999999999
    fiscal_id = 123
    document_name = 'test_pdf_get'

    # Primeiro, inserir um documento para depois buscá-lo
    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:
        document_content = doc.read()
    
    pdf = PDF(document_content, document_name=document_name)
    documents = [pdf]
    
    project_document_repository.insert_fiscal_documents(
        work_project_id=work_project_id, 
        documents=documents
    )

    # Agora obtém o documento
    document = project_document_repository.get_fiscal_document(
        work_project_id=work_project_id,
        fiscal_id=fiscal_id,
        document_name=document_name
    )
    assert document is not None, \
        f"O documento '{document_name}' não foi encontrado para o work_project_id {work_project_id}."

    assert isinstance(document, Document)
    assert document.document_name == document_name, \
        f"O nome do documento retornado não corresponde ao nome esperado."

def test_delete_fiscal_document() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

    work_project_id = 999999999
    fiscal_id = 123
    document_name = 'test_pdf'

    # Deleta o anexo
    project_document_repository.delete_fiscal_document(
        work_project_id=work_project_id,
        fiscal_id=fiscal_id,
        document_name=document_name
    )

    # Verifica se foi deletado
    with db_connection_handler as db:
        key = f'ProjectDocumentsFiscal/{work_project_id}'
        entity = db.load(key)

        if entity is None:
            raise Exception(f'Documento com work_project_id {work_project_id} não encontrado.')

        metadata = db.advanced.get_metadata_for(entity)
        attachments = metadata.get('@attachments', [])

        assert all(att['Name'] != document_name for att in attachments), \
            f"O anexo '{document_name}' ainda está presente no documento."

def test_delete_all_fiscal_documents_from_work_project() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

    work_project_id = 999999999
    fiscal_id = 123

    # Inserir múltiplos documentos de teste
    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:
        document = doc.read()
    
    pdf1 = PDF(document, document_name='test_pdf_1')
    pdf2 = PDF(document, document_name='test_pdf_2')
    documents = [pdf1, pdf2]
    
    project_document_repository.insert_fiscal_documents(
        work_project_id=work_project_id, 
        documents=documents
    )

    # Deleta todos os documentos do work project
    project_document_repository.delete_all_fiscal_documents_from_work_project(
        work_project_id=work_project_id,
        fiscal_id=fiscal_id
    )

    # Verifica se todos foram deletados
    with db_connection_handler as db:
        key = f'ProjectDocumentsFiscal/{work_project_id}'
        entity = db.load(key)

        if entity is None:
            raise Exception(f'Documento com work_project_id {work_project_id} não encontrado.')

        metadata = db.advanced.get_metadata_for(entity)
        attachments = metadata.get('@attachments', [])

        assert len(attachments) == 0, \
            f"Ainda existem anexos no documento após a deleção."

def test_multiple_fiscals_same_work_project() -> None:
    db_connection_handler = DBConnectionHandler(DataConnection())
    project_document_repository = ProjectDocumentFiscalRepository(db_connection_handler)

    work_project_id = 999999999
    fiscal_id_1 = 123
    fiscal_id_2 = 456

    with open('src/infra/raven/repositories/__test/test.pdf', 'rb') as doc:
        document = doc.read()
    
    # Inserir documentos de fiscais diferentes
    pdf1 = PDF(document, document_name='fiscal_1_doc')
    pdf2 = PDF(document, document_name='fiscal_2_doc')
    
    project_document_repository.insert_fiscal_documents(
        work_project_id=work_project_id, 
        documents=[pdf1]
    )
    
    project_document_repository.insert_fiscal_documents(
        work_project_id=work_project_id, 
        documents=[pdf2]
    )

    # Verificar se ambos os documentos estão no mesmo work project
    with db_connection_handler as db:
        key = f'ProjectDocumentsFiscal/{work_project_id}'
        entity = db.load(key)

        if entity is None:
            raise Exception(f'Documento com work_project_id {work_project_id} não encontrado.')

        metadata = db.advanced.get_metadata_for(entity)
        attachments = metadata.get('@attachments', [])

        assert any(att['Name'] == 'fiscal_1_doc' for att in attachments), \
            f"O documento do fiscal 1 não foi encontrado."
        assert any(att['Name'] == 'fiscal_2_doc' for att in attachments), \
            f"O documento do fiscal 2 não foi encontrado."