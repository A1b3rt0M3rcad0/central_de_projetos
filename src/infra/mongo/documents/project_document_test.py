#pylint:disable=C2801
import pytest
from unittest.mock import MagicMock
from src.infra.mongo.documents.project_document import ProjectDocument

@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_db.list_collection_names.return_value = []
    return mock_db

@pytest.fixture
def mock_db_handler(mock_db):
    mock_handler = MagicMock()
    mock_handler.__enter__.return_value = mock_db
    mock_handler.__exit__.return_value = None
    return mock_handler

def test_initialize_creates_collection_and_index(mock_db_handler):
    # Garantir que a flag está em False
    ProjectDocument.init = False

    doc = ProjectDocument(mock_db_handler)

    # Testa se o nome da collection foi consultado
    mock_db_handler.__enter__().list_collection_names.assert_called_once()

    # Testa se a collection foi criada
    mock_db_handler.__enter__().create_collection.assert_called_with('projectdocument')

    # Testa se o índice foi criado
    mock_db_handler.__enter__().__getitem__.return_value.create_index.assert_called_with(
        [('project_id', 1)], unique=True
    )

    # Verifica se a flag foi marcada como True
    assert doc.init is True
