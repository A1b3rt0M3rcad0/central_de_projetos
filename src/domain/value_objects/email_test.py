import pytest
from src.domain.value_objects.email import Email

def test_valid_email() -> None:
    valid_emails = [
        "example@gmail.com",
        "joao@gmail.com",
        "joao1234@gmail.com"
    ]
    for email in valid_emails:
        assert Email(email) == email

def test_invalid_email() -> None:
    invalid_emails = [
        "example@gmail",
        "joao@gmail",
        "joao1234@gmail",
        "@gmail.com",
        "joao1234@gmail..com",
        "joao@.com"
    ]
    for email in invalid_emails:
        with pytest.raises(ValueError):
            Email(email)

def test_string_email() -> None:
    str_email = "example@gmail.com"
    email = Email(str_email)
    assert str(email) == str_email

def test_equal_email() -> None:
    str_email = "example@gmail.com"
    email = Email(str_email)
    email_2 = Email(str_email)
    assert email == email_2