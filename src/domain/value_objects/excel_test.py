import pytest
from src.domain.value_objects.excel import Excel

@pytest.fixture
def sample_excel_bytes():
    # Um exemplo de conteúdo binário simulado para um arquivo .xlsx
    return b'PK\x03\x04 sample excel content'

@pytest.fixture
def another_excel_bytes():
    return b'PK\x03\x04 different excel content'

def test_should_create_excel_with_bytes(sample_excel_bytes):
    excel = Excel(sample_excel_bytes)
    assert excel.xlsx.getvalue() == sample_excel_bytes

def test_should_convert_excel_to_string(sample_excel_bytes):
    excel = Excel(sample_excel_bytes)
    expected_hex = sample_excel_bytes.hex()
    assert str(excel) == expected_hex
    assert repr(excel) == expected_hex

def test_should_compare_equal_excels(sample_excel_bytes):
    excel1 = Excel(sample_excel_bytes)
    excel2 = Excel(sample_excel_bytes)
    assert excel1 == excel2

def test_should_compare_different_excels(sample_excel_bytes, another_excel_bytes):
    excel1 = Excel(sample_excel_bytes)
    excel2 = Excel(another_excel_bytes)
    assert excel1 != excel2

def test_should_compare_excel_with_other_type(sample_excel_bytes):
    excel = Excel(sample_excel_bytes)
    assert excel != 'not an excel file'
    assert excel is not None
    assert excel != bytes()

def test_property_content_type(sample_excel_bytes):
    excel = Excel(sample_excel_bytes)
    assert excel.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

def test_property_excel_name(sample_excel_bytes):
    excel = Excel(sample_excel_bytes)
    assert excel.name == 'document.xlsx'
