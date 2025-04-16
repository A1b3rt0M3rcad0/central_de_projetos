#pylint:disable=all
from src.infra.mongo.config.connection.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.mongo.models.project_document_model import ProjectDocumentModel
from src.infra.mongo.documents.project_document import ProjectDocument
from src.domain.value_objects.pdf import PDF
from src.domain.value_objects.word import Word
from src.domain.value_objects.excel import Excel
from typing import List, Union

class ProjectDocumentRepository:

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    

    def create_project_document(self, project_id:int, documents:List[Union[PDF, Word, Excel]]) -> None:
        return None
    
    def insert_documents_into_project(self, project_id:int, documents:List[Union[PDF, Word, Excel]]) -> None:
        return None
    
    def delete_document_from_project(self, project_id:int, document_name:str) -> None:
        return None