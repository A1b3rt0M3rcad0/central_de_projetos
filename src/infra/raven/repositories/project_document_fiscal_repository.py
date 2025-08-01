from src.domain.value_objects.document import Document
from src.infra.raven.config.connection.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.raven.models.document import DocumentModel
from src.infra.raven.documents.project_document_fiscal import ProjectDocumentsFiscal
from src.data.interface.i_raven_project_document_repository import IProjectDocumentRepository
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository
from datetime import datetime, timezone
from typing import List
import mimetypes
import re

class ProjectDocumentFiscalRepository(IProjectDocumentRepository, IProjectDocumentFiscalRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert_documents(self, project_id:int, project_documents:ProjectDocumentsFiscal, documents:List[Document]):
        with self.__db_connection_handler as db:
            
            project_document_data = project_documents.make_to_store(project_id=project_id)

            db.store(project_document_data['entity'], project_document_data['key'])

            db.save_changes()

            for document in documents:
                ## Document Name With Date
                now = datetime.now(timezone.utc).strftime('%d/%m/%Y')
                document_name = f'{document.document_name}__{now}'
                ## Saving document
                db.advanced.attachments.store(project_document_data['entity'], document_name, document.value(), document.content_type)
                db.save_changes()
    
    def delete_document(self, project_id: int, document_name: str) -> None:
        with self.__db_connection_handler as db:
            
            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)

            entity = db.load(project_document_data["key"])

            db.advanced.attachments.delete(entity, document_name)

            db.save_changes()
    
    def delete_project(self, project_id: int) -> None:
        with self.__db_connection_handler as db:
            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)

            entity = db.load(project_document_data["key"])

            if entity is None:
                raise  RuntimeError('Error on delete project does not exists')

            db.delete(entity)
            db.save_changes()
    
    def get_document_names(self, project_id: int) -> List[str]:
        document_names = []

        with self.__db_connection_handler as db:
            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)
            entity = db.load(project_document_data["key"])

            if entity is None:
                return document_names

            metadata = db.advanced.get_metadata_for(entity)
            attachments = metadata.get('@attachments', [])

            for attachment in attachments:
                name = attachment['Name']
                content_type = attachment.get('ContentType', '')

                ext = mimetypes.guess_extension(content_type) if content_type else None

                # Verifica se o nome já possui uma extensão (ex: .jpg, .jpeg, .pdf etc.)
                already_has_ext = re.search(r"\.\w{2,5}$", name.lower()) is not None

                if ext and not already_has_ext and ext != ".bin":
                    full_name = f"{name}{ext}"
                else:
                    full_name = name

                document_names.append(full_name)

        return document_names

    def get_document(self, project_id:int, document_name:str, _document_class:Document) -> Document:
        with self.__db_connection_handler as db:

            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)
            entity = db.load(project_document_data["key"])

            if entity is None:
                return None

            attachment_result = db.advanced.attachments.get(entity, document_name)
            if attachment_result is None:
                return None
            
            model = DocumentModel(_document_class=_document_class)
            document = model.make_document(document_value=attachment_result.data, document_name=attachment_result.details.name)

            return document

    # Métodos específicos para documentos de fiscais
    def insert_fiscal_documents(self, project_id:int, fiscal_id:int, documents:List[Document]) -> None:
        """
        Insere documentos enviados por um fiscal específico para um projeto.
        """
        with self.__db_connection_handler as db:
            
            project_document_data = ProjectDocumentsFiscal().make_to_store(project_id=project_id)

            db.store(project_document_data['entity'], project_document_data['key'])

            db.save_changes()

            for document in documents:
                ## Document Name With Date and Fiscal ID
                now = datetime.now(timezone.utc).strftime('%d/%m/%Y')
                document_name = f'fiscal_{fiscal_id}_{document.document_name}__{now}'
                ## Saving document
                db.advanced.attachments.store(project_document_data['entity'], document_name, document.value(), document.content_type)
                db.save_changes()

    def get_fiscal_document(self, project_id:int, fiscal_id:int, document_name:str) -> Document:
        """
        Obtém um documento específico enviado por um fiscal.
        """
        with self.__db_connection_handler as db:

            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)
            entity = db.load(project_document_data["key"])

            if entity is None:
                return None

            # Procura pelo documento com prefixo do fiscal
            fiscal_document_name = f'fiscal_{fiscal_id}_{document_name}'
            attachment_result = db.advanced.attachments.get(entity, fiscal_document_name)
            if attachment_result is None:
                return None
            
            model = DocumentModel(_document_class=Document)
            document = model.make_document(document_value=attachment_result.data, document_name=attachment_result.details.name)

            return document

    def get_fiscal_document_names(self, project_id:int, fiscal_id:int) -> List[str]:
        """
        Lista todos os nomes dos documentos enviados por um fiscal para um projeto.
        """
        document_names = []

        with self.__db_connection_handler as db:
            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)
            entity = db.load(project_document_data["key"])

            if entity is None:
                return document_names

            metadata = db.advanced.get_metadata_for(entity)
            attachments = metadata.get('@attachments', [])

            fiscal_prefix = f'fiscal_{fiscal_id}_'
            
            for attachment in attachments:
                name = attachment['Name']
                
                # Filtra apenas documentos do fiscal específico
                if name.startswith(fiscal_prefix):
                    # Remove o prefixo do fiscal para retornar o nome original
                    original_name = name[len(fiscal_prefix):]
                    content_type = attachment.get('ContentType', '')

                    ext = mimetypes.guess_extension(content_type) if content_type else None

                    # Verifica se o nome já possui uma extensão
                    already_has_ext = re.search(r"\.\w{2,5}$", original_name.lower()) is not None

                    if ext and not already_has_ext and ext != ".bin":
                        full_name = f"{original_name}{ext}"
                    else:
                        full_name = original_name

                    document_names.append(full_name)

        return document_names

    def delete_fiscal_document(self, project_id:int, fiscal_id:int, document_name:str) -> None:
        """
        Deleta um documento específico enviado por um fiscal.
        """
        with self.__db_connection_handler as db:
            
            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)

            entity = db.load(project_document_data["key"])

            # Procura pelo documento com prefixo do fiscal
            fiscal_document_name = f'fiscal_{fiscal_id}_{document_name}'
            db.advanced.attachments.delete(entity, fiscal_document_name)

            db.save_changes()

    def delete_all_fiscal_documents_from_project(self, project_id:int, fiscal_id:int) -> None:
        """
        Deleta todos os documentos enviados por um fiscal para um projeto.
        """
        with self.__db_connection_handler as db:
            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)
            entity = db.load(project_document_data["key"])

            if entity is None:
                return

            metadata = db.advanced.get_metadata_for(entity)
            attachments = metadata.get('@attachments', [])

            fiscal_prefix = f'fiscal_{fiscal_id}_'
            
            # Deleta todos os documentos do fiscal específico
            for attachment in attachments:
                name = attachment['Name']
                if name.startswith(fiscal_prefix):
                    db.advanced.attachments.delete(entity, name)

            db.save_changes()