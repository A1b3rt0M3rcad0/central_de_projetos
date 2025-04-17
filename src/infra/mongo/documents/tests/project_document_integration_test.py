#pylint:disable=all
import pytest
from src.infra.mongo.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.mongo.config.connection.t_string_connection import TStringConnection as StringConnection
from src.infra.mongo.documents.project_document import ProjectDocument

@pytest.fixture(scope='module')
def mongo_connection():
    string_conn = StringConnection()
    handler = DBConnectionHandler(string_conn)
    yield handler

    # Cleanup (remove collection após os testes)
    with handler as db:
        db.drop_collection("projectdocument")


def test_project_document_collection_creation(mongo_connection):
    # Executa a inicialização (criação de collection e índice)
    doc = ProjectDocument(mongo_connection)

    with mongo_connection as db:
        assert "projectdocument" in db.list_collection_names()

        indexes = db["projectdocument"].index_information()
        project_id_index = [i for i in indexes.values() if i.get("key") == [('project_id', 1)]]

        assert project_id_index != [], "Index on 'project_id' not created"
        assert project_id_index[0].get("unique") is True
