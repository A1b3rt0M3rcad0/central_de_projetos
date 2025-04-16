from src.infra.mongo.config.connection.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.mongo.models.project_document_model import ProjectDocumentModel
from src.infra.mongo.documents.project_document import ProjectDocument
from pymongo.errors import DuplicateKeyError
from typing import List, Dict

class ProjectDocumentRepository:

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
        self.__project_document = ProjectDocument(db_connection_handler)
    
    def create_project_document(self, project_model:ProjectDocumentModel) -> None:
        try:
            with self.__db_connection_handler as db:
                if db is not None:
                    db[self.__project_document.document].insert_one(
                        project_model.to_dict()
                    )
                    return
                raise ValueError('Connection is None')
        except DuplicateKeyError as e:
            raise ValueError('This Project already exists') from e
    
    def find_project_document(self, project_id:int) -> List[Dict[str, bytes]]:
        try:
            with self.__db_connection_handler as db:
                if db is not None:
                    project_document = db[self.__project_document.document].find_one(
                        {'project_id': project_id}
                    )
                    return project_document['documents']
                raise ValueError('Connection is None')
        except Exception as e:
            raise e
    
    def insert_documents_into_project(self, project_model: ProjectDocumentModel) -> None:
        try:
            with self.__db_connection_handler as db:
                if db is not None:
                    db[self.__project_document.document].update_one(
                        {'project_id': project_model.project_id},
                        {'$push': {'documents': {'$each': [document.to_dict() for document in project_model.documents]}}}
                    )
                    return
                raise ValueError('Connection is None')
        except Exception as e:
            raise e
    
    # def delete_document_from_project(self, project_id:int, document_name:str) -> None:
    #     return None