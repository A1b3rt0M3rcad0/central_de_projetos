#pylint:disable=W0104, W0106
import pytest
from decimal import Decimal
from src.domain.value_objects.monetary_value import MonetaryValue

def test_valid_monetary_value_initialization() -> None:
    valid_values = [
        10.50,
        100,
        Decimal('75.99')
    ]
    for value in valid_values:
        monetary_value = MonetaryValue(value)
        assert isinstance(monetary_value.value, Decimal)

def test_invalid_monetary_value() -> None:
    invalid_values = [
        'invalid',
        [],
        {},
        None
    ]
    for value in invalid_values:
        with pytest.raises(TypeError):
            MonetaryValue(value)

def test_string_representation() -> None:
    monetary_value = MonetaryValue(10.50)
    assert str(monetary_value) == '$10.50'

def test_repr_representation() -> None:
    monetary_value = MonetaryValue(10.50)
    assert repr(monetary_value) == 'MonetaryValue($10.50)'

def test_addition() -> None:
    value1 = MonetaryValue(10.50)
    value2 = MonetaryValue(20.75)
    result = value1 + value2
    assert isinstance(result, MonetaryValue)
    assert result.value == Decimal('31.25')

def test_invalid_addition() -> None:
    value = MonetaryValue(10.50)
    with pytest.raises(TypeError):
        value + 10.50

def test_subtraction() -> None:
    value1 = MonetaryValue(20.75)
    value2 = MonetaryValue(10.50)
    result = value1 - value2
    assert isinstance(result, MonetaryValue)
    assert result.value == Decimal('10.25')

def test_invalid_subtraction() -> None:
    value = MonetaryValue(10.50)
    with pytest.raises(TypeError):
        value - 5.25

def test_multiplication() -> None:
    value = MonetaryValue(10.50)
    result = value * 2
    assert isinstance(result, MonetaryValue)
    assert result.value == Decimal('21.00')

def test_invalid_multiplication() -> None:
    value = MonetaryValue(10.50)
    with pytest.raises(TypeError):
        value * MonetaryValue(2)

def test_division() -> None:
    value = MonetaryValue(21.00)
    result = value / 2
    assert isinstance(result, MonetaryValue)
    assert result.value == Decimal('10.50')

def test_invalid_division() -> None:
    value = MonetaryValue(10.50)
    with pytest.raises(TypeError):
        value / MonetaryValue(2)

def test_division_by_zero() -> None:
    value = MonetaryValue(10.50)
    with pytest.raises(ZeroDivisionError):
        value / 0

def test_reverse_division() -> None:
    value = MonetaryValue(10.50)
    with pytest.raises(ValueError):
        10 / value