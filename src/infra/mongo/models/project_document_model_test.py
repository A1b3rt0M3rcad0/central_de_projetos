import pytest
from src.domain.value_objects.excel import Excel
from src.domain.value_objects.pdf import PDF
from src.domain.value_objects.word import Word
from src.infra.mongo.models.project_document_model import ProjectDocumentModel

@pytest.fixture
def excel_document():
    # Mock de um documento Excel
    return Excel(xlsx=b"Excel content here", document_name='excel')

@pytest.fixture
def pdf_document():
    # Mock de um documento PDF
    return PDF(pdf=b"PDF content here", document_name='pdf')

@pytest.fixture
def word_document():
    # Mock de um documento Word
    return Word(docx=b"Word content here", document_name='word')

@pytest.fixture
def project_document_model(excel_document, pdf_document, word_document):
    # Criando um modelo de documento de projeto
    documents = [excel_document, pdf_document, word_document]
    return ProjectDocumentModel(project_id=123, documents=documents)

def test_project_document_model_creation(project_document_model, excel_document, pdf_document, word_document):
    # Verifica se o ProjectDocumentModel é criado corretamente
    assert project_document_model.project_id == 123
    assert len(project_document_model.documents) == 3
    assert project_document_model.documents[0] == excel_document
    assert project_document_model.documents[1] == pdf_document
    assert project_document_model.documents[2] == word_document

def test_project_document_model_documents_property(project_document_model):
    # Verifica se a propriedade 'documents' retorna os documentos corretamente
    documents = project_document_model.documents
    assert isinstance(documents, list)
    assert len(documents) == 3

def test_project_document_model_project_id_property(project_document_model):
    # Verifica se a propriedade 'project_id' retorna o ID corretamente
    assert project_document_model.project_id == 123

def test_excel_equality(excel_document):
    # Verifica se dois objetos Excel com o mesmo conteúdo são iguais
    excel_2 = Excel(xlsx=b"Excel content here", document_name='excel')
    assert excel_document == excel_2

def test_pdf_equality(pdf_document):
    # Verifica se dois objetos PDF com o mesmo conteúdo são iguais
    pdf_2 = PDF(pdf=b"PDF content here", document_name='pdf')
    assert pdf_document == pdf_2

def test_word_equality(word_document):
    # Verifica se dois objetos Word com o mesmo conteúdo são iguais
    word_2 = Word(docx=b"Word content here", document_name='word')
    assert word_document == word_2

def test_excel_inequality(excel_document):
    # Verifica se dois objetos Excel com conteúdo diferente são diferentes
    excel_2 = Excel(xlsx=b"Different Excel content", document_name='excel')
    assert excel_document != excel_2

def test_pdf_inequality(pdf_document):
    # Verifica se dois objetos PDF com conteúdo diferente são diferentes
    pdf_2 = PDF(pdf=b"Different PDF content", document_name='pdf')
    assert pdf_document != pdf_2

def test_word_inequality(word_document):
    # Verifica se dois objetos Word com conteúdo diferente são diferentes
    word_2 = Word(docx=b"Different Word content", document_name='work')
    assert word_document != word_2

def test_documents_equality_in_project_document(project_document_model, excel_document, pdf_document, word_document):
    # Verifica se a lista de documentos no modelo de documento é igual
    new_project_document = ProjectDocumentModel(
        project_id=123, 
        documents=[excel_document, pdf_document, word_document]
    )
    assert project_document_model == new_project_document

def test_documents_inequality_in_project_document(project_document_model, excel_document, pdf_document, word_document):
    # Verifica se documentos diferentes no modelo de projeto são diferentes
    new_project_document = ProjectDocumentModel(
        project_id=124, 
        documents=[excel_document, pdf_document, word_document]
    )
    assert project_document_model != new_project_document
