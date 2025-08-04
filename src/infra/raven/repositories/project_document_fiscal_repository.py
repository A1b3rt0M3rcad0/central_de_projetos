from src.domain.value_objects.document import Document
from src.infra.raven.config.connection.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.raven.documents.project_document_fiscal import ProjectDocumentsFiscal
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository
from src.domain.value_objects.generic_document import GenericDocument
from typing import List
import mimetypes
import re

class ProjectDocumentFiscalRepository(IProjectDocumentFiscalRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    


    # Métodos específicos para documentos de fiscais
    def insert_fiscal_documents(self, work_project_id:int, fiscal_id:int, documents:List[Document]) -> None:
        """
        Insere documentos enviados por um fiscal específico para um work project.
        """
        with self.__db_connection_handler as db:
            
            project_document_data = ProjectDocumentsFiscal().make_to_store(work_project_id=work_project_id)

            db.store(project_document_data['entity'], project_document_data['key'])

            db.save_changes()

            for document in documents:
                ## Saving document with original name
                document_name = f'{document.document_name}'
                ## Saving document
                db.advanced.attachments.store(project_document_data['entity'], document_name, document.value(), document.content_type)
                db.save_changes()

    def get_fiscal_document(self, work_project_id:int, fiscal_id:int, document_name:str) -> Document:
        """
        Obtém um documento específico enviado por um fiscal.
        """
        with self.__db_connection_handler as db:

            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(work_project_id=work_project_id)
            entity = db.load(project_document_data["key"])

            if entity is None:
                return None

            # Procura pelo documento com nome original
            attachment_result = db.advanced.attachments.get(entity, document_name)
            if attachment_result is None:
                return None
            
            # Cria um documento genérico com os dados
            document = GenericDocument(
                document=attachment_result.data,
                document_name=attachment_result.details.name,
                content_type=attachment_result.details.content_type
            )

            return document

    def get_fiscal_document_names(self, work_project_id:int, fiscal_id:int) -> List[str]:
        """
        Lista todos os nomes dos documentos enviados por um fiscal para um work project.
        """
        document_names = []

        with self.__db_connection_handler as db:
            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(work_project_id=work_project_id)
            entity = db.load(project_document_data["key"])

            if entity is None:
                return document_names

            metadata = db.advanced.get_metadata_for(entity)
            attachments = metadata.get('@attachments', [])

            for attachment in attachments:
                name = attachment['Name']
                content_type = attachment.get('ContentType', '')

                ext = mimetypes.guess_extension(content_type) if content_type else None

                # Verifica se o nome já possui uma extensão
                already_has_ext = re.search(r"\.\w{2,5}$", name.lower()) is not None

                if ext and not already_has_ext and ext != ".bin":
                    full_name = f"{name}{ext}"
                else:
                    full_name = name

                document_names.append(full_name)

        return document_names

    def delete_fiscal_document(self, work_project_id:int, fiscal_id:int, document_name:str) -> None:
        """
        Deleta um documento específico enviado por um fiscal.
        """
        with self.__db_connection_handler as db:
            
            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(work_project_id=work_project_id)

            entity = db.load(project_document_data["key"])

            # Deleta o documento com nome original
            db.advanced.attachments.delete(entity, document_name)

            db.save_changes()

    def delete_all_fiscal_documents_from_work_project(self, work_project_id:int, fiscal_id:int) -> None:
        """
        Deleta todos os documentos enviados por um fiscal para um work project.
        """
        with self.__db_connection_handler as db:
            dummy_project_documents = ProjectDocumentsFiscal()
            project_document_data = dummy_project_documents.make_to_store(work_project_id=work_project_id)
            entity = db.load(project_document_data["key"])

            if entity is None:
                return

            metadata = db.advanced.get_metadata_for(entity)
            attachments = metadata.get('@attachments', [])
            
            # Deleta todos os documentos do work project
            for attachment in attachments:
                name = attachment['Name']
                db.advanced.attachments.delete(entity, name)

            db.save_changes()