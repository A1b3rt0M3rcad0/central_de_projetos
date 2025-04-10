import pytest
from src.domain.value_objects.password import Password

def test_str_password() -> None:
    str_password = '123@Alberto'
    password = Password(str_password)
    assert password == str_password

def test_equal_password() -> None:
    password = Password('123@Alberto')
    password2 = Password('123@Alberto')
    assert password == password2

def test_valid_password_length() -> None:
    with pytest.raises(ValueError):
        Password('1@Ab124')

def test_valid_password_contains_uppercase() -> None:
    with pytest.raises(ValueError):
        Password('1@ab1237')

def test_valid_password_contains_lowercase() -> None:
    with pytest.raises(ValueError):
        Password('1@AB1237')

def test_valid_password_contains_digit() -> None:
    with pytest.raises(ValueError):
        Password('@Abcdefg')

def test_valid_password_contains_empty_space() -> None:
    with pytest.raises(ValueError):
        Password('123@Alberto ')