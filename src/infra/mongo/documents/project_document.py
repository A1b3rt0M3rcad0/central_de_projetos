from src.infra.mongo.config.connection.interface.i_db_connection_handler import IDBConnectionHandler

class ProjectDocument:

    init = False

    def __init__(self, db_connection_handler: IDBConnectionHandler) -> None:
        self.__document = self.__class__.__name__.lower()
        self.__db_connection_handler = db_connection_handler
        self.__initialize()

    def __initialize(self) -> None:
        if not self.init:
            with self.__db_connection_handler as db:
                if db is None:
                    raise ValueError('Database connection not established')
                existing_documents = db.list_collection_names()
                if self.__document not in existing_documents:
                    db.create_collection(self.__document)
                    self.__create_index()
                    self.init = True
    
    def __create_index(self) -> None:
        with self.__db_connection_handler as db:
            if db is not None:
                db[self.__document].create_index(
                    [('project_id', 1)], unique=True
                )
        