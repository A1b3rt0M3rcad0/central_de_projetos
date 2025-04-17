import pytest
from src.domain.value_objects.roles import Role
def test_valid_role() -> None:
    with pytest.raises(ValueError):
        Role('somewhere')
    
def test_valid_role_equal() -> None:
    role = Role('assessor')
    assert role == Role('assessor')

def test_valid_role_string_equal() -> None:
    role = Role('admin')
    assert role == 'ADMIN'