from src.domain.value_objects.excel import Excel
from src.domain.value_objects.word import Word
from src.domain.value_objects.pdf import PDF
from src.infra.raven.config.connection.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.raven.documents.project_documents import ProjectDocuments
from typing import List, Union, Optional

class ProjectDocumentRepository:

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler

    def _create_document_from_data(self, document_data) -> Union[Excel, Word, PDF]:
        """
        Método responsável por criar o documento (Excel, Word ou PDF)
        a partir dos dados extraídos do banco.
        """
        document_name = document_data['document_name']
        document_value = document_data['value']  # Aqui assumimos que 'value' seja o conteúdo do arquivo
        content_type = document_data['content_type']
        
        # Criar o documento com base no tipo de conteúdo
        if content_type == "application/pdf":
            return PDF(document_value, document_name=document_name)
        if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return Word(document_value, document_name=document_name)
        if content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            return Excel(document_value, document_name=document_name)
        raise ValueError(f"Tipo de documento desconhecido: {content_type}")
    
    
    def insert_documents(self, project_id:int, project_documents:ProjectDocuments, documents:List[Union[Optional[Excel | Word | PDF]]]):
        with self.__db_connection_handler as db:
            
            project_document_data = project_documents.make_to_store(project_id=project_id)

            db.store(project_document_data['entity'], project_document_data['key'])

            db.save_changes()

            for document in documents:
                db.advanced.attachment.store(project_document_data['entity'], document.document_name, document.value(), document.content_type)
                db.save_changes()
    
    def delete_document(self, project_id: int, document_name: str) -> None:
        with self.__db_connection_handler as db:
            
            # 1. Criar um ProjectDocuments "fake" só pra poder gerar a chave (key)
            dummy_project_documents = ProjectDocuments(name="", description=None)
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)

            # 2. Carregar o documento pelo ID (key)
            entity = db.load(project_document_data["key"])

            # 3. Deletar o anexo
            db.advanced.attachment.delete(entity, document_name)

            # 4. Salvar alterações
            db.save_changes()
    
    def get_documents_by_project(self, project_id: int) -> List[Union[Excel, Word, PDF]]:
        with self.__db_connection_handler as db:
            dummy_project_documents = ProjectDocuments(name="", description=None)
            project_document_data = dummy_project_documents.make_to_store(project_id=project_id)

            entity = db.load(project_document_data["key"])
            if not entity:
                return []
            
            documents = db.advanced.attachment.get(entity)
            return [self._create_document_from_data(doc) for doc in documents]
