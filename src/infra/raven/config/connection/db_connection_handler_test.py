import pytest
from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler

# Modelo de exemplo
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

@pytest.fixture
def db_session():
    connection = DataConnection()
    handler = DBConnectionHandler(connection)
    with handler as session:
        yield session

def test_store_and_load_document(db_session):
    person = Person(name="Alberto", age=30)
    doc_id = "people/1"

    # Armazena o documento
    db_session.store(person, doc_id)
    db_session.save_changes()

    # Recupera o documento
    loaded = db_session.load(doc_id)

    assert loaded is not None
    assert loaded.name == "Alberto"
    assert loaded.age == 30
