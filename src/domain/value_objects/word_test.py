import pytest
from src.domain.value_objects.word import Word

@pytest.fixture
def sample_word_bytes():
    # Simulando conteúdo binário de um arquivo .docx
    return b'PK\x03\x04 sample word content'

@pytest.fixture
def another_word_bytes():
    return b'PK\x03\x04 different word content'

def test_should_create_word_with_bytes(sample_word_bytes):
    word = Word(sample_word_bytes)
    assert word.docx.getvalue() == sample_word_bytes

def test_should_convert_word_to_string(sample_word_bytes):
    word = Word(sample_word_bytes)
    expected_hex = sample_word_bytes.hex()
    assert str(word) == expected_hex
    assert repr(word) == expected_hex

def test_should_compare_equal_words(sample_word_bytes):
    word1 = Word(sample_word_bytes)
    word2 = Word(sample_word_bytes)
    assert word1 == word2

def test_should_compare_different_words(sample_word_bytes, another_word_bytes):
    word1 = Word(sample_word_bytes)
    word2 = Word(another_word_bytes)
    assert word1 != word2

def test_should_compare_word_with_other_type(sample_word_bytes):
    word = Word(sample_word_bytes)
    assert word != 'not a word file'
    assert word is not None
    assert word != bytes()

def test_property_content_type(sample_word_bytes):
    word = Word(sample_word_bytes)
    assert word.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

def test_property_word_name(sample_word_bytes):
    word = Word(sample_word_bytes)
    assert word.name == 'document.docx'