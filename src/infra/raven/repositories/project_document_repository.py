from src.domain.value_objects.excel import Excel
from src.domain.value_objects.word import Word
from src.domain.value_objects.pdf import PDF
from src.infra.raven.config.connection.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.raven.documents.project_documents import ProjectDocuments
from typing import List, Union, Optional

class ProjectDocumentRepository:

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    
    def insert_documents(self, project_id:int, project_documents:ProjectDocuments, documents:List[Union[Optional[Excel | Word | PDF]]]):
        with self.__db_connection_handler as db:
            
            store = project_documents.make_to_store(project_id=project_id)

            db.store(store['entity'], store['key'])

            db.save_changes()

            for document in documents:
                db.advanced.attachment.store(store['entity'], document.document_name, document.value(), document.content_type)
            
            db.save_changes()