from src.domain.value_objects.cpf import CPF
import pytest
from typing import List

@pytest.fixture
def valid_cpfs() -> List[str]:

    return [
        '687.880.640-26',
        '233.428.200-63',
        '233.428.200-63',
        '23342820063',
    ]

@pytest.fixture
def invalid_cpfs() -> List[str]:

    return [
        '687.880.640-76',
        '233.428.200-83',
        '233.428.200-93',
        '23342820093',
        '1234112312',
        '981273986123891823',
        '11111111111'
    ]

def test_valid_cpfs(valid_cpfs):

    for email in valid_cpfs:
        CPF(email)

def test_invalid_cpfs(invalid_cpfs):

    for email in invalid_cpfs:
        with pytest.raises(ValueError):
            CPF(email)

def test_cpf_value(valid_cpfs):

    n_cpf = valid_cpfs[0].replace('.', '').replace('-', '')
    cpf = CPF(n_cpf)

    assert cpf.value == n_cpf
