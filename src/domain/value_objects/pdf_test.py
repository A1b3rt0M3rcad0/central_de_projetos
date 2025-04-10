import pytest
from src.domain.value_objects.pdf import PDF

@pytest.fixture
def sample_pdf_bytes():
    return b'%PDF-1.4 sample content'

@pytest.fixture
def another_pdf_bytes():
    return b'%PDF-1.4 different content'

def test_should_create_pdf_with_bytes(sample_pdf_bytes):
    pdf = PDF(sample_pdf_bytes)
    assert pdf.pdf.getvalue() == sample_pdf_bytes

def test_should_convert_pdf_to_string(sample_pdf_bytes):
    pdf = PDF(sample_pdf_bytes)
    expected_hex = sample_pdf_bytes.hex()
    assert str(pdf) == expected_hex
    assert repr(pdf) == expected_hex

def test_should_compare_equal_pdfs(sample_pdf_bytes):
    pdf1 = PDF(sample_pdf_bytes)
    pdf2 = PDF(sample_pdf_bytes)
    assert pdf1 == pdf2

def test_should_compare_different_pdfs(sample_pdf_bytes, another_pdf_bytes):
    pdf1 = PDF(sample_pdf_bytes)
    pdf2 = PDF(another_pdf_bytes)
    assert pdf1 != pdf2

def test_should_compare_pdf_with_other_type(sample_pdf_bytes):
    pdf = PDF(sample_pdf_bytes)
    assert pdf != 'not a pdf'
    assert pdf is not None
    assert pdf != bytes()

def test_property_content_type(sample_pdf_bytes):
    pdf = PDF(sample_pdf_bytes)
    assert pdf.content_type == 'application/pdf'

def test_property_pdf_name(sample_pdf_bytes):
    pdf = PDF(sample_pdf_bytes)
    assert pdf.name == 'document.pdf'