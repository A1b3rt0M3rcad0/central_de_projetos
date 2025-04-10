#pylint:disable=all
import pytest
from datetime import datetime
from src.domain.value_objects.timestamp import Timestamp
from src.domain.value_objects.date import Date


def test_valid_timestamp_seconds():
    ts_value = 1712743072  # 10 dígitos (segundos)
    ts = Timestamp(ts_value)
    dt = ts.to_datetime()
    assert isinstance(dt, datetime)
    assert dt.year >= 2020  # ano razoável


def test_valid_timestamp_milliseconds():
    ts_value = 1712743072123  # 13 dígitos (milissegundos)
    ts = Timestamp(ts_value)
    dt = ts.to_datetime()
    assert isinstance(dt, datetime)
    assert dt.year >= 2020


def test_to_date_returns_date_object():
    ts_value = 1712743072
    ts = Timestamp(ts_value)
    date = ts.to_date()
    assert isinstance(date, Date)
    assert date.year() >= 2020


def test_invalid_type_string():
    with pytest.raises(TypeError):
        Timestamp("1712743072")


def test_invalid_type_none():
    with pytest.raises(TypeError):
        Timestamp(None)


def test_negative_timestamp():
    with pytest.raises(ValueError):
        Timestamp(-1000)


def test_unreasonably_large_timestamp():
    with pytest.raises(ValueError):
        # Um timestamp para o ano 3500 em milissegundos
        Timestamp(32503680000 * 1000 + 1)


def test_valid_edge_case_3000_milliseconds():
    # 01/01/3000 em milissegundos (máximo aceitável)
    try:
        Timestamp(32503680000 * 1000)
    except Exception:
        pytest.fail("Timestamp for year 3000 in milliseconds should be valid")
