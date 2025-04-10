import pytest
from src.domain.value_objects.date import Date


def test_valid_date() -> None:
    valid_dates = [
        "01/01/2023",
        "31/12/1999",
        "29/02/2020",  # ano bissexto
    ]
    for date_str in valid_dates:
        assert Date(date_str).to_date().strftime("%d/%m/%Y") == date_str


def test_invalid_date_format() -> None:
    invalid_format_dates = [
        "01012023",
        "2023/01/01",
        "31-12-2023",
        "12/2023",
        "31/12",
        "31//2023",
        "31/12/23",
        "ab/cd/efgh"
    ]
    for date_str in invalid_format_dates:
        with pytest.raises(ValueError):
            Date(date_str)


def test_invalid_date_value() -> None:
    invalid_dates = [
        "32/01/2023",  # dia inválido
        "00/12/2023",  # dia inválido
        "31/04/2023",  # abril tem 30 dias
        "29/02/2021",  # não é ano bissexto
        "15/13/2022",  # mês inválido
    ]
    for date_str in invalid_dates:
        with pytest.raises(ValueError):
            Date(date_str)


def test_string_date() -> None:
    str_date = "15/08/2023"
    dt = Date(str_date)
    assert str(dt) == str_date


def test_equal_date() -> None:
    str_date = "01/01/2023"
    date1 = Date(str_date)
    date2 = Date(str_date)
    assert date1 == date2
